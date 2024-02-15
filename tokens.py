def getBotToken():
    try:
            botTokenFile = open("./.bottoken","r")
    except:
        print("Fichier ./.bottoken introuvable")
        exit()
    BOTTOKEN = botTokenFile.read()
    botTokenFile.close()

    return BOTTOKEN

def getApiCrToken():
    try:
        apiCrTokenFile = open("./.apicrtoken","r")
    except:
        print("Fichier ./.apicrtoken introuvable")
        exit()
    APICRTOKEN = apiCrTokenFile.read()
    apiCrTokenFile.close()

    return APICRTOKEN
