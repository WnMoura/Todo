from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin

from .models import Todo
from .serializers import TodoSerializer


class TodoListView(
  APIView,
  UpdateModelMixin, 
  DestroyModelMixin, 
):

  def get(self, request, id=None):
    if id:
      try:
        queryset = Todo.objects.get(id=id)
      except Todo.DoesNotExist:
        return Response({'errors': 'This todo item does not exist.'}, status=400)

      
      read_serializer = TodoSerializer(queryset)

    else:
      
      queryset = Todo.objects.all()

      read_serializer = TodoSerializer(queryset, many=True)

    return Response(read_serializer.data)


  def post(self, request):
    create_serializer = TodoSerializer(data=request.data)

    if create_serializer.is_valid():

      todo_item_object = create_serializer.save()

      read_serializer = TodoSerializer(todo_item_object)

      return Response(read_serializer.data, status=201)

    return Response(create_serializer.errors, status=400)


  def put(self, request, id=None):
    try:
      todo_item = Todo.objects.get(id=id)
    except Todo.DoesNotExist:
      return Response({'errors': 'This todo item does not exist.'}, status=400)

    update_serializer = TodoSerializer(todo_item, data=request.data)

    if update_serializer.is_valid():

      todo_item_object = update_serializer.save()

      read_serializer = TodoSerializer(todo_item_object)

      return Response(read_serializer.data, status=200)

    return Response(update_serializer.errors, status=400)


  def delete(self, request, id=None):
    try:
      todo_item = Todo.objects.get(id=id)
    except Todo.DoesNotExist:
      return Response({'errors': 'This todo item does not exist.'}, status=400)

    todo_item.delete()

    return Response(status=204)