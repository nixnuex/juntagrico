from django.shortcuts import render, redirect

from juntagrico.dao.depotdao import DepotDao
from juntagrico.dao.memberdao import MemberDao
from juntagrico.dao.subscriptionproductdao import SubscriptionProductDao
from juntagrico.dao.subscriptiontypedao import SubscriptionTypeDao
from juntagrico.forms import *
from juntagrico.models import *
from juntagrico.util import temporal
from juntagrico.util.create_sub import get_main_member
from juntagrico.util.management import *


def cs_welcome(request):
    main_member = get_main_member(request)
    if main_member is None:
        return redirect('http://'+Config.server_url())

    renderdict = {
        'no_subscription': main_member.future_subscription is None
    }

    return render(request, 'welcome.html', renderdict)


def cs_select_subscription(request, multi=False):
    main_member = get_main_member(request)
    if main_member is None:
        return redirect('http://'+Config.server_url())
    if request.method == 'POST':
        # create dict with subscription type -> selected amount
        selected = {
            sub_type: int(
                request.POST.get('amount[' + str(sub_type.id) + ']',  # if multi selection
                                 int(request.POST.get('subscription', -1)) == sub_type.id)  # if single selection
            ) for sub_type in SubscriptionTypeDao.get_all()
        }
        request.session['selected_subscriptions'] = selected
        if sum([sub_type.size.units * amount for sub_type, amount in selected.items()]) > 0:
            return redirect('/my/create/subscription/selectdepot')
        return redirect('/my/create/subscription/shares')
    renderdict = {
        'hours_used': Config.assignment_unit() == 'HOURS',
        'products': SubscriptionProductDao.get_all(),
        'multi_edit': multi and Config.allow_multiple_subscriptions(),
    }
    return render(request, 'createsubscription/select_subscription.html', renderdict)


def cs_select_depot(request):
    main_member = get_main_member(request)
    if main_member is None:
        return redirect('http://'+Config.server_url())
    if request.method == 'POST':
        depot = DepotDao.depot_by_id(request.POST.get('depot'))
        request.session['selecteddepot'] = depot
        return redirect('/my/create/subscription/start')
    depots = DepotDao.all_depots()
    requires_map = True
    for depot in depots:
        requires_map = requires_map or depot.has_geo
    renderdict = {
        'member': main_member,
        'depots': depots,
        'requires_map': requires_map,
    }
    return render(request, 'createsubscription/select_depot.html', renderdict)


def cs_select_start_date(request):
    main_member = get_main_member(request)
    if main_member is None:
        return redirect('http://'+Config.server_url())
    subscriptionform = SubscriptionForm()
    if request.method == 'POST':
        subscriptionform = SubscriptionForm(request.POST)
        if subscriptionform.is_valid():
            request.session['start_date'] = subscriptionform.cleaned_data['start_date']
            return redirect('/my/create/subscription/addmembers')
    renderdict = {
        'start_date': temporal.start_of_next_business_year(),
        'subscriptionform': subscriptionform,
    }
    return render(request, 'createsubscription/select_start_date.html', renderdict)


def cs_select_shares(request):
    main_member = get_main_member(request)
    if main_member is None:
        return redirect('http://'+Config.server_url())
    share_error = False
    mm_requires_one = len(main_member.active_shares) == 0
    share_sum = len(main_member.active_shares)
    co_members = request.session.get('create_co_members', [])
    for co_member in co_members:
        share_sum += len(co_member.active_shares)
    selected_subscriptions = request.session.get('selected_subscriptions', {})
    total_shares = sum([sub_type.shares * amount for sub_type, amount in selected_subscriptions.items()])
    required_shares = max(0, total_shares-max(0, share_sum))

    if request.method == 'POST' or not Config.enable_shares():
        try:
            share_sum = int(request.POST.get('shares_mainmember'))
            for co_member in co_members:
                share_sum += int(request.POST.get(co_member.email))
            share_error = share_error or share_sum < required_shares
            share_error = share_error or (int(request.POST.get('shares_mainmember')) == 0 and mm_requires_one)
        except ValueError:
            share_error = True
        if not share_error or not Config.enable_shares():
            subscription = None
            if selected_subscriptions is not {}:
                start_date = request.session['start_date']
                depot = request.session['selecteddepot']
                subscription = create_subscription(
                    start_date, depot, selected_subscriptions)
            if main_member.pk is None:
                create_member(main_member, subscription)
            else:
                update_member(main_member, subscription)
            if Config.enable_shares():
                shares = int(request.POST.get('shares_mainmember'))
            else:
                shares = 0
            for i in range(shares):
                create_share(main_member)
            for co_member in co_members:
                if Config.enable_shares():
                    shares = int(request.POST.get(co_member.email))
                else:
                    shares = 0
                if co_member.pk is None:
                    create_member(co_member, subscription, main_member, shares)
                else:
                    update_member(co_member, subscription, main_member, shares)
                for i in range(shares):
                    create_share(co_member)
            if subscription is not None:
                subscription.primary_member = main_member
                subscription.save()
                send_subscription_created_mail(subscription)
            request.session['selected_subscriptions'] = None
            request.session['selecteddepot'] = None
            request.session['start_date'] = None
            request.session['create_co_members'] = []
            if request.user.is_authenticated:
                return redirect('/my/subscription/detail/')
            else:
                return redirect('/my/welcome')
    renderdict = {
        'share_error': share_error,
        'total_shares': total_shares,
        'required_shares': required_shares,
        'member': main_member,
        'co_members': co_members,
        'has_com_members': len(co_members) > 0,
        'mm_requires_one': mm_requires_one
    }
    return render(request, 'createsubscription/select_shares.html', renderdict)


def cs_add_member(request):
    main_member = get_main_member(request)
    if main_member is None:
        return redirect('http://'+Config.server_url())
    memberexists = False
    memberblocked = False
    co_members = request.session.get('create_co_members', [])
    if request.method == 'POST':
        memberform = RegisterMemberForm(request.POST)
        member = next(iter(MemberDao.members_by_email(
            request.POST.get('email')) or []), None)
        if member is not None:
            memberexists = True
            memberblocked = member.blocked
        if memberform.is_valid()or (memberexists is True and memberblocked is False):
            if memberexists is False:
                member = Member(**memberform.cleaned_data)
            co_members.append(member)
            request.session['create_co_members'] = co_members
    initial = {'addr_street': main_member.addr_street,
               'addr_zipcode': main_member.addr_zipcode,
               'addr_location': main_member.addr_location,
               }
    memberform = RegisterMemberForm(initial=initial)
    renderdict = {
        'memberexists': memberexists,
        'memberblocked': memberblocked,
        'memberform': memberform,
    }
    return render(request, 'createsubscription/add_member_cs.html', renderdict)


def cs_cancel_create_subscription(request):
    request.session['main_member'] = None
    request.session['selected_subscription'] = None
    request.session['selecteddepot'] = None
    request.session['start_date'] = None
    request.session['create_co_members'] = []
    if request.user.is_authenticated:
        return redirect('/my/subscription/detail/')
    else:
        return redirect('http://'+Config.server_url())
