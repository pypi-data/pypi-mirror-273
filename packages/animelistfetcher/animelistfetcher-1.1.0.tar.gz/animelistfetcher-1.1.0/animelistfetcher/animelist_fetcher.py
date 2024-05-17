import time

def get_userdata(service, service_token = None):
    service = service.lower()
    if service == "al" or service == "anilist":
        import alfetcher
        return alfetcher.get_userdata(service_token)
    elif service == "mal" or service == "myanimelist":
        import malfetcher
        return malfetcher.get_userdata(service_token)

def clear_cache(service):
    service = service.lower()
    if service == "al" or service == "anilist":
        import alfetcher
        return alfetcher.clear_cache()
    elif service == "mal" or service == "myanimelist":
        import malfetcher
        return malfetcher.clear_cache()

def config():
    import alfetcher, malfetcher
    print("Starting AniList setup")
    alfetcher.config_setup()
    time.sleep(5)
    print("Starting MyAnimeList setup")
    malfetcher.config_setup()

def get_latest_anime_entry_for_user(service, status = "ALL", service_token = None, username = None):
    service = service.lower()
    if service == "al" or service == "anilist":
        import alfetcher
        return alfetcher.get_latest_anime_entry_for_user(status, service_token, username)
    elif service == "mal" or service == "myanimelist":
        import malfetcher
        return malfetcher.get_latest_anime_entry_for_user(status, service_token, username)

def get_all_anime_for_user(service, status_array = "ALL", service_token = None, username = None):
    service = service.lower()
    if service == "al" or service == "anilist":
        import alfetcher
        return alfetcher.get_all_anime_for_user(status_array, service_token, username)
    elif service == "mal" or service == "myanimelist":
        import malfetcher
        return malfetcher.get_all_anime_for_user(status_array, service_token, username)

def get_anime_entry_for_user(service, anime_id, service_token = None, username = None):
    service = service.lower()
    if service == "al" or service == "anilist":
        import alfetcher
        return alfetcher.get_anime_entry_for_user(anime_id, service_token, username)
    elif service == "mal" or service == "myanimelist":
        import malfetcher
        return malfetcher.get_anime_entry_for_user(anime_id, service_token)

def get_anime_info(service, anime_id, service_token = None):
    service = service.lower()
    if service == "al" or service == "anilist":
        import alfetcher
        return alfetcher.get_anime_info(anime_id, False, service_token)
    elif service == "mal" or service == "myanimelist":
        import malfetcher
        return malfetcher.get_anime_info(anime_id, False, service_token)

def get_id(service, search_string, service_token = None):
    service = service.lower()
    if service == "al" or service == "anilist":
        import alfetcher
        return alfetcher.get_id(search_string, service_token)
    elif service == "mal" or service == "myanimelist":
        import malfetcher
        return malfetcher.get_id(search_string, service_token)

def update_entry(service, anime_id, progress, service_token=None):
    service = service.lower()
    if service == "al" or service == "anilist":
        import alfetcher
        return alfetcher.update_entry(anime_id, progress, service_token)
    elif service == "mal" or service == "myanimelist":
        import malfetcher
        return malfetcher.update_entry(anime_id, progress, service_token)