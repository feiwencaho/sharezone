
from django.views import View
from common.utils.http import formatting
from api.auth.decorator import auth
import ujson
from api import service
from api.const import ShareStatus
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from api.core.serializers import ShareSerializer
from api.views import BaseView


class Shares(BaseView):
    @formatting()
    @auth
    def post(self, request):
        """
        发布共享
        :param request:
        :return:
        """
        data = request.data
        share = service.share.publish(request.user, **data)
        return ShareSerializer(share).data

    @formatting()
    @auth
    def get(self, request):
        """
        我发布的共享
        :param request:
        :return:
        """
        user = request.user
        shares = service.share.get_shares(user=user)
        return [ShareSerializer(share).data for share in shares]


class PublicShares(BaseView):

    @formatting()
    def get(self, request):
        """
        所有用户已发布的共享
        :param request:
        :return:
        """
        shares = service.share.get_shares(status=ShareStatus.OPEN)
        return [ShareSerializer(share).data for share in shares]


class Share(BaseView):
    @formatting()
    def get(self, request, share_id):
        """
        共享详情
        :param request:
        :param share_id:
        :return:
        """
        share = service.share.get_share(id=share_id)
        return ShareSerializer(share).data
