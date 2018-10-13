from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist
from crawlapp.models import Domain, Crawledpages
from crawlapp.utils import Crawlutils
import json


class DomainsAPI(View):
    """
        endpoint: '/api/v1/domain/'
        req params: None
        resp: [{"id": , "name: example.com"}, {}, {},]
    """
    def get(self, request, domain_id=None):
        if domain_id:
            try:
                domain = Domain.objects.get(id=domain_id)

                # get crawled pages and return to frontend
                cobjs = Crawledpages.objects.filter(domain_id=domain_id)
                master_list = []

                # form response format
                for item in cobjs:
                    di = dict()
                    di["url"] = item.url
                    di["links"] = json.loads(item.page_links)
                    di["image_links"] = json.loads(item.image_links)
                    master_list.append(di)

                return JsonResponse({"domain": {"id": domain.id, "name": domain.name}, "success": True,
                                     "summary": "Crawled info", "crawled": master_list})
            except ObjectDoesNotExist as e:
                return JsonResponse({"domain": {}, "success": False, "summary": "Domain not found", "crawled": []})
        else:
            domains = Domain.objects.all()
            data = [{"id": i.id, "name": i.name} for i in domains]
            return JsonResponse({"domains": data, "success": True, "summary": "Domains info"})


@method_decorator(csrf_exempt, name='dispatch')
class CrawlAPI(View):
    """
            endpoint: '/api/v1/crawl/'
            req params: {"url": "http://google.co.in/", "depth": 1}
            resp: json response
        """
    def post(self, request):
        root_url = request.POST.get("url", "")
        depth = int(request.POST.get("depth", 0))

        response_dict = {"success": True, "domain": {}}

        if "http" not in root_url or not root_url:
            response_dict["success"] = False
            return JsonResponse(response_dict)

        # crawl with crawl utils
        c = Crawlutils()
        resp_dict = c.crawl(start_url=root_url, max_depth=depth)

        # create or get domain
        domain = resp_dict["domain"]
        dobj, created = Domain.objects.get_or_create(name=domain)
        domain_id = dobj.id

        # insert crawled links and pages
        results = resp_dict["results"]
        for depth, url, data, found_urls, img_urls in results:
            try:
                cobj = Crawledpages()
                cobj.domain_id = domain_id
                cobj.content = data
                cobj.page_links = json.dumps(found_urls)
                cobj.image_links = json.dumps(img_urls)
                if url == root_url:
                    cobj.is_seed_url = True
                cobj.save()
            except Exception as e:
                continue
        response_dict["domain"] = {"id": domain_id, "name": dobj.name}
        return JsonResponse(response_dict)