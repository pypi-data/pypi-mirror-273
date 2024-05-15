from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import ExtraFileUploadForm
class IndexView(View):
    def get(self, request):
        return render(request, 'extra_files/index.html')

class UploadView(View):
    def get(self, request):
        cid = request.GET.get('object_id')
        form = ExtraFileUploadForm(initial={'circuit': cid})
        return render(request, 'extra_files/upload.html', { 'form': form })
    def post(self, request):
        form = ExtraFileUploadForm(request.POST, request.FILES)
        form.save()
        return redirect('/circuits/circuits/{}'.format(request.POST.get('circuit')))
