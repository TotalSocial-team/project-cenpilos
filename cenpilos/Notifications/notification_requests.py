from cenpilos.scripts import version_info


def notifications_get_request():

    # version information
    version = version_info.version_information()
    version_type, stage, v_type, number = version[0], version[1], version[2], version[3]

    # extra variables to be passed to the initial screen
    return {
        'stage': stage,
        'type': v_type,
        'number': number,
        'version_type': version_type,
        'notifications': 'active',
    }


