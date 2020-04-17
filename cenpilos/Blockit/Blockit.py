def getStatus() -> list:
    protected_status = 0
    # protected status, numerical value to value displayed to the user: #
    # if protected_status variable is:
    # 0 == protected (no action needed)
    # 1 == warning to be displayed to the user (might require user to take action)
    # 2 == not protected (immediate action required)

    # displayed underneath the account status
    description = ""

    # the colour of the description
    d_colour = ''

    if protected_status == 0:
        description = 'Great news! We have not found any problems with you account. ' \
                      'However, please check here for regular updates.'
        d_colour = 'success'

    return [protected_status, description, d_colour]