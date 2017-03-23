def get_status_image(percent=0):
    if percent >= 100:
        return "circle_full.png"
    elif percent >= 75:
        return "circle_alomst_full.png"
    elif percent >= 50:
        return "circle_half.png"
    elif percent > 0:
        return "circle_almost_empty.png"
    else:
        return "circle_empty.png"


def get_status_image_text(percent=0):
    if percent >= 100:
        return "Fertig"
    elif percent >= 75:
        return "Dreiviertel"
    elif percent >= 50:
        return "Halb"
    elif percent > 0:
        return "Angefangen"
    else:
        return "Nix"