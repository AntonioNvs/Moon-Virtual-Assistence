from Functions.Web_Scraping import portal_notas, corona_virus, clima
from Functions.Musics import playist
from Functions.Sites import acessar, main_search
from Functions.YouTube import acessar_musica


def controll_function(text, language) -> bool:
    portal_notas.detection_portal_notas(text, language)
    corona_virus.detection_corona_virus(text, language)
    playist.detection_playist(text, language)
    clima.detection_clima(text, language)
    acessar.detection_acessar(text, language)
    main_search.detection_search(text, language)
    # baixar_video.detection_video(text, language)
    # baixar_musica.detection_baixar_musica(text, language)
    acessar_musica.detection_acessar_musica(text, language)
    return True


if __name__ == '__main__':
    pass
