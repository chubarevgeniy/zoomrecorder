
ZOOM = True
TEAMS = True
# If language is ru use 'tasklist /fo table /v /fi "imagename eq msteams.exe" /fi "windowtitle eq Собр*"' 
#   instead of 'tasklist /fo table /v /fi "imagename eq msteams.exe" /fi "windowtitle eq Meet*"'

# Note: Need the /v for verbose. /fi filters the process and looks for window title for Teams meeting
def tasklist_query():
    if ZOOM is True and TEAMS is False:
        query = 'tasklist /fo table /v /fi "imagename eq CptHost.exe"'
    elif ZOOM is False and TEAMS is True: 
        #query = 'tasklist /fo table /v /fi "imagename eq Teams.exe" /fi "windowtitle eq Meet*"'
        query = 'tasklist /fo table /v /fi "imagename eq msteams.exe" /fi "windowtitle eq Meet*"'
    else:
        query = 'tasklist /fo table /v /fi "imagename eq CptHost.exe" && ' \
                'tasklist /fo table /v /fi "imagename eq msteams.exe" /fi "windowtitle eq Meet*"'
                #'tasklist /fo table /v /fi "imagename eq Teams.exe" /fi "windowtitle eq Meet*" /nh'

    return query