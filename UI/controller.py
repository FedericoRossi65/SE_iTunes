import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model
        self.selezione = None

    def handle_crea_grafo(self, e):
        self._view.lista_visualizzazione_1.clean()
        durata = int(self._view.txt_durata.value)
        if durata > 0:
            self._model.build_graph(durata)
            nodi,archi = self._model.graph_det()
            self._view.lista_visualizzazione_1.controls.append(ft.Text(f'I nodi sono: {nodi}, e archi : {archi}'))
            album = self._model.load_album(int(self._view.txt_durata.value))
            for a in album:
                self._view.dd_album.options.append(ft.dropdown.Option(key=a.id,text=a))
        else:
            self._view.show_alert(f'Inserisci un valore intero')
        self._view.update()
    def get_selected_album(self, e):
        """ Handler per gestire la selezione dell'album dal dropdown """""
        self.selezione = self._model.id_map[int(self._view.dd_album.value)]

    def handle_analisi_comp(self, e):
        """ Handler per gestire l'analisi della componente connessa """""
        self._view.lista_visualizzazione_2.clean()
        c = self._model.get_component(self.selezione)
        self._view.lista_visualizzazione_2.controls.append(ft.Text(f'Dimensione compenente: {len(c)}'))
        durata_tot = 0
        for a in c:
            durata_tot += round(a.duration,2)
        self._view.lista_visualizzazione_2.controls.append(ft.Text(f'Durata totale: {durata_tot}'))
        self._view.update()


    def handle_get_set_album(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del set di album """""
        # TODO