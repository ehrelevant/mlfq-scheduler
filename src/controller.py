from model import MLFQModel
from view import MLFQView

class MLFQController:
    _model: MLFQModel
    _view: MLFQView
    
    def __init__(self, model: MLFQModel, view: MLFQView):
        self._model = model
        self._view = view

    def begin_simulation(self):
        view = self._view
        model = self._model

        curr_scheduler_details: tuple[int, int, int, int] = view.request_scheduler_details()
        model.implement_scheduler_details(curr_scheduler_details)

        curr_process_details: list[str] = view.request_process_details(model.num_processes)
        model.implement_process_details(curr_process_details)

        model.setup_priority_queues()
        model.setup_mlfq()

        #view.on_tick()
        #model.do_smth_on_tick()

        view.output(model.mlfq)
