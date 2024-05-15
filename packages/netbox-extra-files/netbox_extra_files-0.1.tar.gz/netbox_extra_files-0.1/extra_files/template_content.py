from extras.plugins import PluginTemplateExtension
from .models import ExtraFile

class CircuitExtraFiles(PluginTemplateExtension):

    model='circuits.circuit'

    def right_page(self):

        files = ExtraFile.objects.filter(circuit=self.context['object'])
        return self.render('extra_files/circuits/list.html', extra_context = {'files': files})

template_extensions = [CircuitExtraFiles]
