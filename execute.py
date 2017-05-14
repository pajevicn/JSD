from textx.metamodel import metamodel_from_file
from textx.export import metamodel_export, model_export
import pydot, os


def execute(path, grammar_file_name, example_file_name, export_dot, export_png):
    '''U svrhe brzeg testiranja, metoda koja prima putanju do foldera, naziv fajla gdje je gramatika i naziv fajla gdje je 
        primjer programa u nasem jeziku i indikator da li da se eksportuju .dot i .png fajlovi'''

    meta_path = os.path.join(path, grammar_file_name)
    meta_name = os.path.splitext(meta_path)[0]
    metamodel = metamodel_from_file(meta_path)

    if export_dot:
        metamodel_export(metamodel, meta_name + '.dot')
        if export_png:
            graph = pydot.graph_from_dot_file(meta_name + '.dot')
            # graph[0].write_png(meta_name + '.png')

    model_path = os.path.join(path, example_file_name)
    model_name = os.path.splitext(model_path)[0]
    model = metamodel.model_from_file(model_path)

    if export_dot:
        model_export(model, model_name + '.dot')
    if export_png:
        graph = pydot.graph_from_dot_file(model_name + '.dot')
        # graph[0].write_png(model_name + '.png')

    # u ovom dijelu generisemo views.py file i klase i funkcije vezane za taj fajl
    def function(model):
        string = 'from django.views import generic\nfrom django.views.generic.edit import CreateView, UpdateView, DeleteView\nfrom django.core.urlresolvers import reverse_lazy, reverse\n'
        string += '\n'
        for m in model:
            string += 'from .models import ' + m.name + '\n'
        #Generator za createview
        for m in model:
            string += '\n'
            string += 'class ' + m.name + 'CreateView(CreateView):'
            string += '\n\t'
            string += 'template_name' + '=' + "'.html'" + '\n\t'
            string += 'model' + '=' + m.name + '\n\t'
            string += 'fields = ['
            last = len(m.elements) - 1
            for i, element in enumerate(m.elements):
                string += "'" + element.name + "'"
                if i == last:
                    string += ']'
                else:
                    string += ', '
            string += '\n\t' + "success_url=reverse_lazy('')"
            string += '\n\n'

            # Generator za updateview
            string += '\n'
            string += 'class ' + m.name + 'UpdateView(UpdateView):'
            string += '\n\t'
            string += 'template_name' + '=' + "'.html'" + '\n\t'
            string += 'model' + '=' + m.name + '\n\t'
            string += 'fields = ['
            last = len(m.elements) - 1
            for i, element in enumerate(m.elements):
                string +="'" + element.name + "'"
                if i == last:
                    string += ']'
                else:
                    string += ', '
            string += '\n\n'

            # Generator za deleteview
            string += '\n'
            string += 'class ' + m.name + 'DeleteView(DeleteView):'
            string += '\n\t'
            string += 'template_name' + '=' + "'.html'" + '\n\t'
            string += 'model' + '=' + m.name + '\n\t'
            string += "success_url=reverse_lazy('')"
            string += '\n\n'

            # Generator za listview
            string += '\n'
            string += 'class ' + m.name + 'ListView(generic.ListView):'
            string += '\n\t'
            string += 'template_name' + ' = ' + "'.html'" + '\n\t'
            string += 'context_object_name' + ' = ' + "'" + 'all_' + m.name + "'" + '\n\t'
            string += 'def ' + 'get_queryset(self):' + '\n\t\t'
            string += 'return ' + m.name + '.object.all'
            string += '\n\n'

        return string
    with open('views.py', 'w') as f:
        a = function(model.models)
        f.write(a)

    # u ovom dijelu generisemo models.py file, klase i funkcije vezane za taj fajl
    def functionM(model):
        string = 'import os\nfrom django.db import models\n'
        string += '\n'
        for m in model:
            string += '\n'
            string += 'class ' + m.name + '(models.Model):\t'
            for i, element in enumerate(m.elements):
                    string += '\n\t'
                    string += element.name + " = " + "models."

                    if element.datatype.foreignkey is not None:
                        string += 'ForeignKey(' + element.name + ', ' + 'on_delete=models.CASCADE)'
                    elif element.datatype.CharField is not None:
                        string += 'CharField('
                        if len(element.datatype.CharField.parameters) == 0:
                            string += ")),"
                        elif len(element.datatype.CharField.parameters) == 1:
                            if element.datatype.CharField.parameters[0].max_length is not None:
                                string += 'max_length=' + element.datatype.CharField.parameters[
                                    0].max_length.number + "),"
                            if element.datatype.CharField.parameters[0].null is not None:
                                string += 'null=' + element.datatype.CharField.parameters[0].null.value + "),"
                        elif len(element.datatype.CharField.parameters) == 3:
                            string += 'max_length=' + element.datatype.CharField.parameters[0].max_length.number + ", "
                            string += 'null=' + element.datatype.CharField.parameters[1].null.value + ", "
                        elif element.datatype.CharField.parameters[0].max_length and element.datatype.CharField.parameters[1].null is not None:
                            string += 'max_length=' + element.datatype.CharField.parameters[0].max_length.number + ", "
                            string += 'null=' + element.datatype.CharField.parameters[1].null.value + ")"
                    elif element.datatype.EmailField is not None:
                        string += 'EmailField('

                        if len(element.datatype.EmailField.parameters) == 0:
                            string += ")"
                        elif len(element.datatype.EmailField.parameters) == 1:
                            if element.datatype.EmailField.parameters[0].max_length is not None:
                                string += 'max_length=' + element.datatype.EmailField.parameters[0].max_length.number + '),'

        return string
    with open('models.py', 'w') as f:
        a = functionM(model.models)
        f.write(a)

    # dio gdje se generise urls.py
    def functionU(model):
        string = 'from django.conf.urls import url\nfrom . import views\n'
        string += '\n' + 'app_name = ' + "'" + 'JSD' + "'"
        string += '\n\nurlpatterns = [' + '\n\n'
        string +=']'

        return string

    with open('urls.py', 'w') as f:
        a = functionU(model)
        f.write(a)

     # Kreiranje templates foldera
    newpath = r'templates'
    if not os.path.exists(newpath):
            os.makedirs(newpath)

    # genersianje sablona u okviru foldera templates
    def functionB(model):
        string = '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n<title>{% block title %} JSD PROJEKAT {% endblock %}</title>\n<body>\n{% block body %}\n{% endblock %}\n</body>\n</html>'

        return string
    with open('templates/base.html', 'w') as f:
        a = functionB(model)
        f.write(a)

    def functionB(model):
        string = "{% extends 'base.html' %}\n{% block title %} Prva strana {% endblock %}\n{% block body %}\n{% endblock %}"

        return string
    with open('templates/index.html', 'w') as f:
        a = functionB(model)
        f.write(a)

    # generator koda za admin.py
    def functionA(model):
        string = 'from django.contrib import admin\n'
        string += 'from .models import '
        last = len(model) - 1
        for i,model in enumerate(model):
            string += model.name
            if i == last:
                string += '' + '\n'
            else:
                string += ', '
        string += '' + '\n'
        string += 'admin.site.register(' + model.name + ')'
        return string
    with open('admin.py', 'w') as f:
        a = functionA(model.models)
        f.write(a)