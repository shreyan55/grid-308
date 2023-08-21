from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.http import JsonResponse
from typing import Any
import json
from operator import itemgetter

from apps.user.models import Customer
from apps.interaction.models import Interaction,Result
from apps.product.models import Product, Category
from ml.recomendation_model import recommend_items
from django.shortcuts import get_object_or_404

class SimulationView(TemplateView):
    template_name = 'simulation/index.html'
    queryset = Interaction

    def get_context_data(self,user_id, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["actions"] = Interaction.InteractionChoices
        context["user_id"]=user_id
        return context

    
class ProductListView(View):
    def post(self, request, *args, **kwargs):
        try:
            data=json.loads(request.body)
            products = Product.objects.filter(category__id=int(data.get('category_id')))
            products = [{"name": product.product_name, "pid": product.pid} for product in products]
            return JsonResponse({'products': products}, status = 201)
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)})
        

class CreateInteractionAPIView(View):
    def post(self, request, user_id):
        try:
            customer = Customer.objects.get(id=user_id)
            data=json.loads(request.body)
            print(customer)
            for interaction in data.get('interactions'):
                pid=interaction["product_id"]
                event=interaction["interaction"]
                rating=interaction.get('rating')
                print("rating",rating)
                product=Product.objects.get(pid=pid,)
                obj = Interaction(product=product, customer=customer, interaction=event, rating=rating)
                obj.save()
            rated_items=recommend_items(user_id=user_id)
            print("rated",rated_items)
            item_json=json.dumps(rated_items)
            print(item_json)
            result=Result.objects.create(data=item_json,customer=customer)
            print("result_id",result)
            return JsonResponse({'result_id': result.id}, status = 201)
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)})
        
   

class ResultView(View):

    def get(self, request,result_id, **kwargs):
        
        # customer=get_object_or_404(Customer,)
        results = get_object_or_404(Result, id=result_id)
        
        
        product_data = []  # To store product details (product_id, timestamp, and weight)

        # # Iterate through each result
        
        result_data =json.loads(results.data)  # Assuming it's a dictionary
        print("result_Data",result_data)
        for product_id in result_data:
            print(product_id)
            weight = result_data[product_id]
            try:
                product = Product.objects.get(pid=product_id)
                
                product_data.append({
                    'product_id': product.pid,
                    'timestamp': results.timestamp,
                    'weight': weight,
                    'product_name': product.product_name,  # You can add more product details here
                    'product_url': product.product_url,
                })
            except Product.DoesNotExist:
                # Handle the case where the product with the given ID does not exist
                pass
        product_data = sorted(product_data, key=itemgetter('weight'), reverse=True)
        print(product_data)
        return render(request,'results/result.html',{'product_data':product_data})


class HistoryView(View):
    def get(self, request,user_id, **kwargs):
        history=Result.objects.filter(customer__id=user_id)
        print("history",history)
        return render(request,'history/history.html',{'user_id':user_id,'history':history})    


class ReportsView(View):
    def get(self, request,user_id, **kwargs):
        return render(request,'reports/reports.html',{'user_id':user_id})