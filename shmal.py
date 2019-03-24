from Pymoe import Kitsu
import Setup

instance = Kitsu(Setup.kitsu_client_id, Setup.kitsu_client_secret)

search = instance.anime.search("Jojo")  # Search anime by term
print(search)
print(search[1]['attributes']['posterImage']['small'])
print(search[1]['attributes']['titles']['en_jp'])
print(search[1]['attributes']['titles']['en'])
print(search[1]['attributes']['synopsis'])
print(search[1]['attributes']['startDate'])
print(search[1]['attributes']['endDate'])
print(search[1]['attributes']['ageRatingGuide'])
print(search[1]['attributes']['status'])
print(search[1]['attributes']['posterImage']['small'])

#for tag in len(anime):
#    print(tag)

