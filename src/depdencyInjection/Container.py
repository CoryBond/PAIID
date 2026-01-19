from dependency_injector import containers, providers
from imageProviders.DalleProvider import DalleProvider
from repoManager.RepoManager import RepoManager
from speechRecognition.GoogleSpeachRecognizer import GoogleSpeechRecognizer
from ui.widgets.MainWindow import MainWindow
from ui.QApplicationManager import QApplicationManager
from ui.UIOrchestrator import UIOrchestrator
from ui.widgets.home.HomePage import HomePage
from ui.widgets.gallery.GalleryPage import GalleryPage
from ui.widgets.settings.SettingsPage import SettingsPage

from utils.pathingUtils import get_project_root

from utils.pageUtils import PageDictType, PageName, PageCaption, PageHint, PageMetaDecorator


class PagesDispatcher:
    pages: PageDictType


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    dalleKeyFile = open(get_project_root()/".."/"dalle.key", "r")
    dalleKey = dalleKeyFile.read()
    imageProvider = providers.Singleton(
        DalleProvider,
        key=dalleKey
    )

    qApplicationManager = providers.Singleton(
        QApplicationManager
    )

    speechRecognizer = providers.Singleton(
        GoogleSpeechRecognizer
    )

    repoManager = providers.Singleton(
        RepoManager,
        config.repos.imageReposPath,
        config.repos.startingRepo,
    )

    home = providers.Singleton(HomePage, repoManager, imageProvider, speechRecognizer)
    gallery = providers.Singleton(GalleryPage, repoManager)
    settings = providers.Singleton(SettingsPage)

    homePageMeta = providers.Singleton(PageMetaDecorator, home, PageName.HOME, PageCaption.HOME, PageHint.HOME)
    galleryPageMeta = providers.Singleton(PageMetaDecorator, gallery, PageName.GALLERY, PageCaption.GALLERY, PageHint.GALLERY)
    settingsPageMeta = providers.Singleton(PageMetaDecorator, settings, PageName.SETTINGS, PageCaption.SETTINGS, PageHint.SETTINGS)

    mainWindow = providers.Singleton(
        MainWindow,
        homePageMeta,
        galleryPageMeta,
        settingsPageMeta
    )

    uiOrchestrator = providers.Singleton(
        UIOrchestrator,
        qApplicationManager,
        home,
        gallery,
        mainWindow
    )