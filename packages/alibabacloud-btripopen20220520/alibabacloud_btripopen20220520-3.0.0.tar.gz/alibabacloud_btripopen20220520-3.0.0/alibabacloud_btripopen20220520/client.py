# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
from typing import Dict
from Tea.core import TeaCore

from alibabacloud_tea_openapi.client import Client as OpenApiClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util.client import Client as UtilClient
from alibabacloud_endpoint_util.client import Client as EndpointUtilClient
from alibabacloud_btripopen20220520 import models as btrip_open_20220520_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_openapi_util.client import Client as OpenApiUtilClient


class Client(OpenApiClient):
    """
    *\
    """
    def __init__(
        self, 
        config: open_api_models.Config,
    ):
        super().__init__(config)
        self._endpoint_rule = ''
        self.check_config(config)
        self._endpoint = self.get_endpoint('btripopen', self._region_id, self._endpoint_rule, self._network, self._suffix, self._endpoint_map, self._endpoint)

    def get_endpoint(
        self,
        product_id: str,
        region_id: str,
        endpoint_rule: str,
        network: str,
        suffix: str,
        endpoint_map: Dict[str, str],
        endpoint: str,
    ) -> str:
        if not UtilClient.empty(endpoint):
            return endpoint
        if not UtilClient.is_unset(endpoint_map) and not UtilClient.empty(endpoint_map.get(region_id)):
            return endpoint_map.get(region_id)
        return EndpointUtilClient.get_endpoint_rules(product_id, region_id, endpoint_rule, network, suffix)

    def access_token_with_options(
        self,
        request: btrip_open_20220520_models.AccessTokenRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.AccessTokenResponse:
        """
        @summary 换取accessToken接口
        
        @param request: AccessTokenRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: AccessTokenResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.app_secret):
            query['app_secret'] = request.app_secret
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='AccessToken',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/btrip-open-auth/v1/access-token/action/take',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.AccessTokenResponse(),
            self.call_api(params, req, runtime)
        )

    async def access_token_with_options_async(
        self,
        request: btrip_open_20220520_models.AccessTokenRequest,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.AccessTokenResponse:
        """
        @summary 换取accessToken接口
        
        @param request: AccessTokenRequest
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: AccessTokenResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.app_secret):
            query['app_secret'] = request.app_secret
        req = open_api_models.OpenApiRequest(
            headers=headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='AccessToken',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/btrip-open-auth/v1/access-token/action/take',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.AccessTokenResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def access_token(
        self,
        request: btrip_open_20220520_models.AccessTokenRequest,
    ) -> btrip_open_20220520_models.AccessTokenResponse:
        """
        @summary 换取accessToken接口
        
        @param request: AccessTokenRequest
        @return: AccessTokenResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.access_token_with_options(request, headers, runtime)

    async def access_token_async(
        self,
        request: btrip_open_20220520_models.AccessTokenRequest,
    ) -> btrip_open_20220520_models.AccessTokenResponse:
        """
        @summary 换取accessToken接口
        
        @param request: AccessTokenRequest
        @return: AccessTokenResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.access_token_with_options_async(request, headers, runtime)

    def add_invoice_entity_with_options(
        self,
        tmp_req: btrip_open_20220520_models.AddInvoiceEntityRequest,
        headers: btrip_open_20220520_models.AddInvoiceEntityHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.AddInvoiceEntityResponse:
        """
        @summary 新增发票抬头适用人员
        
        @param tmp_req: AddInvoiceEntityRequest
        @param headers: AddInvoiceEntityHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: AddInvoiceEntityResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.AddInvoiceEntityShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.entities):
            request.entities_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.entities, 'entities', 'json')
        body = {}
        if not UtilClient.is_unset(request.entities_shrink):
            body['entities'] = request.entities_shrink
        if not UtilClient.is_unset(request.third_part_id):
            body['third_part_id'] = request.third_part_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='AddInvoiceEntity',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/invoice/v1/entities',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.AddInvoiceEntityResponse(),
            self.call_api(params, req, runtime)
        )

    async def add_invoice_entity_with_options_async(
        self,
        tmp_req: btrip_open_20220520_models.AddInvoiceEntityRequest,
        headers: btrip_open_20220520_models.AddInvoiceEntityHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.AddInvoiceEntityResponse:
        """
        @summary 新增发票抬头适用人员
        
        @param tmp_req: AddInvoiceEntityRequest
        @param headers: AddInvoiceEntityHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: AddInvoiceEntityResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.AddInvoiceEntityShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.entities):
            request.entities_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.entities, 'entities', 'json')
        body = {}
        if not UtilClient.is_unset(request.entities_shrink):
            body['entities'] = request.entities_shrink
        if not UtilClient.is_unset(request.third_part_id):
            body['third_part_id'] = request.third_part_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='AddInvoiceEntity',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/invoice/v1/entities',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.AddInvoiceEntityResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def add_invoice_entity(
        self,
        request: btrip_open_20220520_models.AddInvoiceEntityRequest,
    ) -> btrip_open_20220520_models.AddInvoiceEntityResponse:
        """
        @summary 新增发票抬头适用人员
        
        @param request: AddInvoiceEntityRequest
        @return: AddInvoiceEntityResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.AddInvoiceEntityHeaders()
        return self.add_invoice_entity_with_options(request, headers, runtime)

    async def add_invoice_entity_async(
        self,
        request: btrip_open_20220520_models.AddInvoiceEntityRequest,
    ) -> btrip_open_20220520_models.AddInvoiceEntityResponse:
        """
        @summary 新增发票抬头适用人员
        
        @param request: AddInvoiceEntityRequest
        @return: AddInvoiceEntityResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.AddInvoiceEntityHeaders()
        return await self.add_invoice_entity_with_options_async(request, headers, runtime)

    def address_get_with_options(
        self,
        request: btrip_open_20220520_models.AddressGetRequest,
        headers: btrip_open_20220520_models.AddressGetHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.AddressGetResponse:
        """
        @summary 商旅功能页跳转
        
        @param request: AddressGetRequest
        @param headers: AddressGetHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: AddressGetResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.action_type):
            query['action_type'] = request.action_type
        if not UtilClient.is_unset(request.arr_city_code):
            query['arr_city_code'] = request.arr_city_code
        if not UtilClient.is_unset(request.arr_city_name):
            query['arr_city_name'] = request.arr_city_name
        if not UtilClient.is_unset(request.car_scenes_code):
            query['car_scenes_code'] = request.car_scenes_code
        if not UtilClient.is_unset(request.dep_city_code):
            query['dep_city_code'] = request.dep_city_code
        if not UtilClient.is_unset(request.dep_city_name):
            query['dep_city_name'] = request.dep_city_name
        if not UtilClient.is_unset(request.dep_date):
            query['dep_date'] = request.dep_date
        if not UtilClient.is_unset(request.itinerary_id):
            query['itinerary_id'] = request.itinerary_id
        if not UtilClient.is_unset(request.order_id):
            query['order_Id'] = request.order_id
        if not UtilClient.is_unset(request.phone):
            query['phone'] = request.phone
        if not UtilClient.is_unset(request.sub_corp_id):
            query['sub_corp_id'] = request.sub_corp_id
        if not UtilClient.is_unset(request.taobao_callback_url):
            query['taobao_callback_url'] = request.taobao_callback_url
        if not UtilClient.is_unset(request.traveler_id):
            query['traveler_id'] = request.traveler_id
        if not UtilClient.is_unset(request.type):
            query['type'] = request.type
        if not UtilClient.is_unset(request.use_booking_proxy):
            query['use_booking_proxy'] = request.use_booking_proxy
        if not UtilClient.is_unset(request.user_id):
            query['user_id'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='AddressGet',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/open/v1/address',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.AddressGetResponse(),
            self.call_api(params, req, runtime)
        )

    async def address_get_with_options_async(
        self,
        request: btrip_open_20220520_models.AddressGetRequest,
        headers: btrip_open_20220520_models.AddressGetHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.AddressGetResponse:
        """
        @summary 商旅功能页跳转
        
        @param request: AddressGetRequest
        @param headers: AddressGetHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: AddressGetResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.action_type):
            query['action_type'] = request.action_type
        if not UtilClient.is_unset(request.arr_city_code):
            query['arr_city_code'] = request.arr_city_code
        if not UtilClient.is_unset(request.arr_city_name):
            query['arr_city_name'] = request.arr_city_name
        if not UtilClient.is_unset(request.car_scenes_code):
            query['car_scenes_code'] = request.car_scenes_code
        if not UtilClient.is_unset(request.dep_city_code):
            query['dep_city_code'] = request.dep_city_code
        if not UtilClient.is_unset(request.dep_city_name):
            query['dep_city_name'] = request.dep_city_name
        if not UtilClient.is_unset(request.dep_date):
            query['dep_date'] = request.dep_date
        if not UtilClient.is_unset(request.itinerary_id):
            query['itinerary_id'] = request.itinerary_id
        if not UtilClient.is_unset(request.order_id):
            query['order_Id'] = request.order_id
        if not UtilClient.is_unset(request.phone):
            query['phone'] = request.phone
        if not UtilClient.is_unset(request.sub_corp_id):
            query['sub_corp_id'] = request.sub_corp_id
        if not UtilClient.is_unset(request.taobao_callback_url):
            query['taobao_callback_url'] = request.taobao_callback_url
        if not UtilClient.is_unset(request.traveler_id):
            query['traveler_id'] = request.traveler_id
        if not UtilClient.is_unset(request.type):
            query['type'] = request.type
        if not UtilClient.is_unset(request.use_booking_proxy):
            query['use_booking_proxy'] = request.use_booking_proxy
        if not UtilClient.is_unset(request.user_id):
            query['user_id'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='AddressGet',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/open/v1/address',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.AddressGetResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def address_get(
        self,
        request: btrip_open_20220520_models.AddressGetRequest,
    ) -> btrip_open_20220520_models.AddressGetResponse:
        """
        @summary 商旅功能页跳转
        
        @param request: AddressGetRequest
        @return: AddressGetResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.AddressGetHeaders()
        return self.address_get_with_options(request, headers, runtime)

    async def address_get_async(
        self,
        request: btrip_open_20220520_models.AddressGetRequest,
    ) -> btrip_open_20220520_models.AddressGetResponse:
        """
        @summary 商旅功能页跳转
        
        @param request: AddressGetRequest
        @return: AddressGetResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.AddressGetHeaders()
        return await self.address_get_with_options_async(request, headers, runtime)

    def airport_search_with_options(
        self,
        request: btrip_open_20220520_models.AirportSearchRequest,
        headers: btrip_open_20220520_models.AirportSearchHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.AirportSearchResponse:
        """
        @summary 查询机场数据
        
        @param request: AirportSearchRequest
        @param headers: AirportSearchHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: AirportSearchResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.keyword):
            query['keyword'] = request.keyword
        if not UtilClient.is_unset(request.type):
            query['type'] = request.type
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='AirportSearch',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/city/v1/airport',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.AirportSearchResponse(),
            self.call_api(params, req, runtime)
        )

    async def airport_search_with_options_async(
        self,
        request: btrip_open_20220520_models.AirportSearchRequest,
        headers: btrip_open_20220520_models.AirportSearchHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.AirportSearchResponse:
        """
        @summary 查询机场数据
        
        @param request: AirportSearchRequest
        @param headers: AirportSearchHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: AirportSearchResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.keyword):
            query['keyword'] = request.keyword
        if not UtilClient.is_unset(request.type):
            query['type'] = request.type
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='AirportSearch',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/city/v1/airport',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.AirportSearchResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def airport_search(
        self,
        request: btrip_open_20220520_models.AirportSearchRequest,
    ) -> btrip_open_20220520_models.AirportSearchResponse:
        """
        @summary 查询机场数据
        
        @param request: AirportSearchRequest
        @return: AirportSearchResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.AirportSearchHeaders()
        return self.airport_search_with_options(request, headers, runtime)

    async def airport_search_async(
        self,
        request: btrip_open_20220520_models.AirportSearchRequest,
    ) -> btrip_open_20220520_models.AirportSearchResponse:
        """
        @summary 查询机场数据
        
        @param request: AirportSearchRequest
        @return: AirportSearchResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.AirportSearchHeaders()
        return await self.airport_search_with_options_async(request, headers, runtime)

    def all_base_city_info_query_with_options(
        self,
        headers: btrip_open_20220520_models.AllBaseCityInfoQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.AllBaseCityInfoQueryResponse:
        """
        @summary 全量查询商旅城市行政区划编码信息
        
        @param headers: AllBaseCityInfoQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: AllBaseCityInfoQueryResponse
        """
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_access_token):
            real_headers['x-acs-btrip-access-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers
        )
        params = open_api_models.Params(
            action='AllBaseCityInfoQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/city/v1/code',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.AllBaseCityInfoQueryResponse(),
            self.call_api(params, req, runtime)
        )

    async def all_base_city_info_query_with_options_async(
        self,
        headers: btrip_open_20220520_models.AllBaseCityInfoQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.AllBaseCityInfoQueryResponse:
        """
        @summary 全量查询商旅城市行政区划编码信息
        
        @param headers: AllBaseCityInfoQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: AllBaseCityInfoQueryResponse
        """
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_access_token):
            real_headers['x-acs-btrip-access-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers
        )
        params = open_api_models.Params(
            action='AllBaseCityInfoQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/city/v1/code',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.AllBaseCityInfoQueryResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def all_base_city_info_query(self) -> btrip_open_20220520_models.AllBaseCityInfoQueryResponse:
        """
        @summary 全量查询商旅城市行政区划编码信息
        
        @return: AllBaseCityInfoQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.AllBaseCityInfoQueryHeaders()
        return self.all_base_city_info_query_with_options(headers, runtime)

    async def all_base_city_info_query_async(self) -> btrip_open_20220520_models.AllBaseCityInfoQueryResponse:
        """
        @summary 全量查询商旅城市行政区划编码信息
        
        @return: AllBaseCityInfoQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.AllBaseCityInfoQueryHeaders()
        return await self.all_base_city_info_query_with_options_async(headers, runtime)

    def apply_add_with_options(
        self,
        tmp_req: btrip_open_20220520_models.ApplyAddRequest,
        headers: btrip_open_20220520_models.ApplyAddHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.ApplyAddResponse:
        """
        @summary 新建出差审批单
        
        @param tmp_req: ApplyAddRequest
        @param headers: ApplyAddHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: ApplyAddResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.ApplyAddShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.car_rule):
            request.car_rule_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.car_rule, 'car_rule', 'json')
        if not UtilClient.is_unset(tmp_req.external_traveler_list):
            request.external_traveler_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.external_traveler_list, 'external_traveler_list', 'json')
        if not UtilClient.is_unset(tmp_req.external_traveler_standard):
            request.external_traveler_standard_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.external_traveler_standard, 'external_traveler_standard', 'json')
        if not UtilClient.is_unset(tmp_req.hotel_share):
            request.hotel_share_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.hotel_share, 'hotel_share', 'json')
        if not UtilClient.is_unset(tmp_req.itinerary_list):
            request.itinerary_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.itinerary_list, 'itinerary_list', 'json')
        if not UtilClient.is_unset(tmp_req.itinerary_set_list):
            request.itinerary_set_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.itinerary_set_list, 'itinerary_set_list', 'json')
        if not UtilClient.is_unset(tmp_req.traveler_list):
            request.traveler_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.traveler_list, 'traveler_list', 'json')
        if not UtilClient.is_unset(tmp_req.traveler_standard):
            request.traveler_standard_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.traveler_standard, 'traveler_standard', 'json')
        body = {}
        if not UtilClient.is_unset(request.budget):
            body['budget'] = request.budget
        if not UtilClient.is_unset(request.budget_merge):
            body['budget_merge'] = request.budget_merge
        if not UtilClient.is_unset(request.car_rule_shrink):
            body['car_rule'] = request.car_rule_shrink
        if not UtilClient.is_unset(request.corp_name):
            body['corp_name'] = request.corp_name
        if not UtilClient.is_unset(request.depart_id):
            body['depart_id'] = request.depart_id
        if not UtilClient.is_unset(request.depart_name):
            body['depart_name'] = request.depart_name
        if not UtilClient.is_unset(request.extend_field):
            body['extend_field'] = request.extend_field
        if not UtilClient.is_unset(request.external_traveler_list_shrink):
            body['external_traveler_list'] = request.external_traveler_list_shrink
        if not UtilClient.is_unset(request.external_traveler_standard_shrink):
            body['external_traveler_standard'] = request.external_traveler_standard_shrink
        if not UtilClient.is_unset(request.flight_budget):
            body['flight_budget'] = request.flight_budget
        if not UtilClient.is_unset(request.hotel_budget):
            body['hotel_budget'] = request.hotel_budget
        if not UtilClient.is_unset(request.hotel_share_shrink):
            body['hotel_share'] = request.hotel_share_shrink
        if not UtilClient.is_unset(request.international_flight_cabins):
            body['international_flight_cabins'] = request.international_flight_cabins
        if not UtilClient.is_unset(request.itinerary_list_shrink):
            body['itinerary_list'] = request.itinerary_list_shrink
        if not UtilClient.is_unset(request.itinerary_rule):
            body['itinerary_rule'] = request.itinerary_rule
        if not UtilClient.is_unset(request.itinerary_set_list_shrink):
            body['itinerary_set_list'] = request.itinerary_set_list_shrink
        if not UtilClient.is_unset(request.limit_traveler):
            body['limit_traveler'] = request.limit_traveler
        if not UtilClient.is_unset(request.payment_department_id):
            body['payment_department_id'] = request.payment_department_id
        if not UtilClient.is_unset(request.payment_department_name):
            body['payment_department_name'] = request.payment_department_name
        if not UtilClient.is_unset(request.status):
            body['status'] = request.status
        if not UtilClient.is_unset(request.sub_corp_id):
            body['sub_corp_id'] = request.sub_corp_id
        if not UtilClient.is_unset(request.thirdpart_apply_id):
            body['thirdpart_apply_id'] = request.thirdpart_apply_id
        if not UtilClient.is_unset(request.thirdpart_business_id):
            body['thirdpart_business_id'] = request.thirdpart_business_id
        if not UtilClient.is_unset(request.thirdpart_depart_id):
            body['thirdpart_depart_id'] = request.thirdpart_depart_id
        if not UtilClient.is_unset(request.together_book_rule):
            body['together_book_rule'] = request.together_book_rule
        if not UtilClient.is_unset(request.train_budget):
            body['train_budget'] = request.train_budget
        if not UtilClient.is_unset(request.traveler_list_shrink):
            body['traveler_list'] = request.traveler_list_shrink
        if not UtilClient.is_unset(request.traveler_standard_shrink):
            body['traveler_standard'] = request.traveler_standard_shrink
        if not UtilClient.is_unset(request.trip_cause):
            body['trip_cause'] = request.trip_cause
        if not UtilClient.is_unset(request.trip_day):
            body['trip_day'] = request.trip_day
        if not UtilClient.is_unset(request.trip_title):
            body['trip_title'] = request.trip_title
        if not UtilClient.is_unset(request.type):
            body['type'] = request.type
        if not UtilClient.is_unset(request.union_no):
            body['union_no'] = request.union_no
        if not UtilClient.is_unset(request.user_id):
            body['user_id'] = request.user_id
        if not UtilClient.is_unset(request.user_name):
            body['user_name'] = request.user_name
        if not UtilClient.is_unset(request.vehicle_budget):
            body['vehicle_budget'] = request.vehicle_budget
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='ApplyAdd',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/apply/v1/biz-trip',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.ApplyAddResponse(),
            self.call_api(params, req, runtime)
        )

    async def apply_add_with_options_async(
        self,
        tmp_req: btrip_open_20220520_models.ApplyAddRequest,
        headers: btrip_open_20220520_models.ApplyAddHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.ApplyAddResponse:
        """
        @summary 新建出差审批单
        
        @param tmp_req: ApplyAddRequest
        @param headers: ApplyAddHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: ApplyAddResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.ApplyAddShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.car_rule):
            request.car_rule_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.car_rule, 'car_rule', 'json')
        if not UtilClient.is_unset(tmp_req.external_traveler_list):
            request.external_traveler_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.external_traveler_list, 'external_traveler_list', 'json')
        if not UtilClient.is_unset(tmp_req.external_traveler_standard):
            request.external_traveler_standard_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.external_traveler_standard, 'external_traveler_standard', 'json')
        if not UtilClient.is_unset(tmp_req.hotel_share):
            request.hotel_share_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.hotel_share, 'hotel_share', 'json')
        if not UtilClient.is_unset(tmp_req.itinerary_list):
            request.itinerary_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.itinerary_list, 'itinerary_list', 'json')
        if not UtilClient.is_unset(tmp_req.itinerary_set_list):
            request.itinerary_set_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.itinerary_set_list, 'itinerary_set_list', 'json')
        if not UtilClient.is_unset(tmp_req.traveler_list):
            request.traveler_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.traveler_list, 'traveler_list', 'json')
        if not UtilClient.is_unset(tmp_req.traveler_standard):
            request.traveler_standard_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.traveler_standard, 'traveler_standard', 'json')
        body = {}
        if not UtilClient.is_unset(request.budget):
            body['budget'] = request.budget
        if not UtilClient.is_unset(request.budget_merge):
            body['budget_merge'] = request.budget_merge
        if not UtilClient.is_unset(request.car_rule_shrink):
            body['car_rule'] = request.car_rule_shrink
        if not UtilClient.is_unset(request.corp_name):
            body['corp_name'] = request.corp_name
        if not UtilClient.is_unset(request.depart_id):
            body['depart_id'] = request.depart_id
        if not UtilClient.is_unset(request.depart_name):
            body['depart_name'] = request.depart_name
        if not UtilClient.is_unset(request.extend_field):
            body['extend_field'] = request.extend_field
        if not UtilClient.is_unset(request.external_traveler_list_shrink):
            body['external_traveler_list'] = request.external_traveler_list_shrink
        if not UtilClient.is_unset(request.external_traveler_standard_shrink):
            body['external_traveler_standard'] = request.external_traveler_standard_shrink
        if not UtilClient.is_unset(request.flight_budget):
            body['flight_budget'] = request.flight_budget
        if not UtilClient.is_unset(request.hotel_budget):
            body['hotel_budget'] = request.hotel_budget
        if not UtilClient.is_unset(request.hotel_share_shrink):
            body['hotel_share'] = request.hotel_share_shrink
        if not UtilClient.is_unset(request.international_flight_cabins):
            body['international_flight_cabins'] = request.international_flight_cabins
        if not UtilClient.is_unset(request.itinerary_list_shrink):
            body['itinerary_list'] = request.itinerary_list_shrink
        if not UtilClient.is_unset(request.itinerary_rule):
            body['itinerary_rule'] = request.itinerary_rule
        if not UtilClient.is_unset(request.itinerary_set_list_shrink):
            body['itinerary_set_list'] = request.itinerary_set_list_shrink
        if not UtilClient.is_unset(request.limit_traveler):
            body['limit_traveler'] = request.limit_traveler
        if not UtilClient.is_unset(request.payment_department_id):
            body['payment_department_id'] = request.payment_department_id
        if not UtilClient.is_unset(request.payment_department_name):
            body['payment_department_name'] = request.payment_department_name
        if not UtilClient.is_unset(request.status):
            body['status'] = request.status
        if not UtilClient.is_unset(request.sub_corp_id):
            body['sub_corp_id'] = request.sub_corp_id
        if not UtilClient.is_unset(request.thirdpart_apply_id):
            body['thirdpart_apply_id'] = request.thirdpart_apply_id
        if not UtilClient.is_unset(request.thirdpart_business_id):
            body['thirdpart_business_id'] = request.thirdpart_business_id
        if not UtilClient.is_unset(request.thirdpart_depart_id):
            body['thirdpart_depart_id'] = request.thirdpart_depart_id
        if not UtilClient.is_unset(request.together_book_rule):
            body['together_book_rule'] = request.together_book_rule
        if not UtilClient.is_unset(request.train_budget):
            body['train_budget'] = request.train_budget
        if not UtilClient.is_unset(request.traveler_list_shrink):
            body['traveler_list'] = request.traveler_list_shrink
        if not UtilClient.is_unset(request.traveler_standard_shrink):
            body['traveler_standard'] = request.traveler_standard_shrink
        if not UtilClient.is_unset(request.trip_cause):
            body['trip_cause'] = request.trip_cause
        if not UtilClient.is_unset(request.trip_day):
            body['trip_day'] = request.trip_day
        if not UtilClient.is_unset(request.trip_title):
            body['trip_title'] = request.trip_title
        if not UtilClient.is_unset(request.type):
            body['type'] = request.type
        if not UtilClient.is_unset(request.union_no):
            body['union_no'] = request.union_no
        if not UtilClient.is_unset(request.user_id):
            body['user_id'] = request.user_id
        if not UtilClient.is_unset(request.user_name):
            body['user_name'] = request.user_name
        if not UtilClient.is_unset(request.vehicle_budget):
            body['vehicle_budget'] = request.vehicle_budget
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='ApplyAdd',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/apply/v1/biz-trip',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.ApplyAddResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def apply_add(
        self,
        request: btrip_open_20220520_models.ApplyAddRequest,
    ) -> btrip_open_20220520_models.ApplyAddResponse:
        """
        @summary 新建出差审批单
        
        @param request: ApplyAddRequest
        @return: ApplyAddResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.ApplyAddHeaders()
        return self.apply_add_with_options(request, headers, runtime)

    async def apply_add_async(
        self,
        request: btrip_open_20220520_models.ApplyAddRequest,
    ) -> btrip_open_20220520_models.ApplyAddResponse:
        """
        @summary 新建出差审批单
        
        @param request: ApplyAddRequest
        @return: ApplyAddResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.ApplyAddHeaders()
        return await self.apply_add_with_options_async(request, headers, runtime)

    def apply_approve_with_options(
        self,
        request: btrip_open_20220520_models.ApplyApproveRequest,
        headers: btrip_open_20220520_models.ApplyApproveHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.ApplyApproveResponse:
        """
        @summary 更新出差审批单（状态）
        
        @param request: ApplyApproveRequest
        @param headers: ApplyApproveHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: ApplyApproveResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.apply_id):
            body['apply_id'] = request.apply_id
        if not UtilClient.is_unset(request.note):
            body['note'] = request.note
        if not UtilClient.is_unset(request.operate_time):
            body['operate_time'] = request.operate_time
        if not UtilClient.is_unset(request.status):
            body['status'] = request.status
        if not UtilClient.is_unset(request.sub_corp_id):
            body['sub_corp_id'] = request.sub_corp_id
        if not UtilClient.is_unset(request.user_id):
            body['user_id'] = request.user_id
        if not UtilClient.is_unset(request.user_name):
            body['user_name'] = request.user_name
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='ApplyApprove',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/apply/v1/biz-trip/action/approve',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.ApplyApproveResponse(),
            self.call_api(params, req, runtime)
        )

    async def apply_approve_with_options_async(
        self,
        request: btrip_open_20220520_models.ApplyApproveRequest,
        headers: btrip_open_20220520_models.ApplyApproveHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.ApplyApproveResponse:
        """
        @summary 更新出差审批单（状态）
        
        @param request: ApplyApproveRequest
        @param headers: ApplyApproveHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: ApplyApproveResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.apply_id):
            body['apply_id'] = request.apply_id
        if not UtilClient.is_unset(request.note):
            body['note'] = request.note
        if not UtilClient.is_unset(request.operate_time):
            body['operate_time'] = request.operate_time
        if not UtilClient.is_unset(request.status):
            body['status'] = request.status
        if not UtilClient.is_unset(request.sub_corp_id):
            body['sub_corp_id'] = request.sub_corp_id
        if not UtilClient.is_unset(request.user_id):
            body['user_id'] = request.user_id
        if not UtilClient.is_unset(request.user_name):
            body['user_name'] = request.user_name
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='ApplyApprove',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/apply/v1/biz-trip/action/approve',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.ApplyApproveResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def apply_approve(
        self,
        request: btrip_open_20220520_models.ApplyApproveRequest,
    ) -> btrip_open_20220520_models.ApplyApproveResponse:
        """
        @summary 更新出差审批单（状态）
        
        @param request: ApplyApproveRequest
        @return: ApplyApproveResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.ApplyApproveHeaders()
        return self.apply_approve_with_options(request, headers, runtime)

    async def apply_approve_async(
        self,
        request: btrip_open_20220520_models.ApplyApproveRequest,
    ) -> btrip_open_20220520_models.ApplyApproveResponse:
        """
        @summary 更新出差审批单（状态）
        
        @param request: ApplyApproveRequest
        @return: ApplyApproveResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.ApplyApproveHeaders()
        return await self.apply_approve_with_options_async(request, headers, runtime)

    def apply_external_node_status_update_with_options(
        self,
        tmp_req: btrip_open_20220520_models.ApplyExternalNodeStatusUpdateRequest,
        headers: btrip_open_20220520_models.ApplyExternalNodeStatusUpdateHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.ApplyExternalNodeStatusUpdateResponse:
        """
        @summary 外部审批节点状态同步
        
        @param tmp_req: ApplyExternalNodeStatusUpdateRequest
        @param headers: ApplyExternalNodeStatusUpdateHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: ApplyExternalNodeStatusUpdateResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.ApplyExternalNodeStatusUpdateShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.operation_records):
            request.operation_records_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.operation_records, 'operation_records', 'json')
        body = {}
        if not UtilClient.is_unset(request.node_id):
            body['node_id'] = request.node_id
        if not UtilClient.is_unset(request.operation_records_shrink):
            body['operation_records'] = request.operation_records_shrink
        if not UtilClient.is_unset(request.process_action_result):
            body['process_action_result'] = request.process_action_result
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='ApplyExternalNodeStatusUpdate',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/apply/v1/external-nodes/action/status-update',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.ApplyExternalNodeStatusUpdateResponse(),
            self.call_api(params, req, runtime)
        )

    async def apply_external_node_status_update_with_options_async(
        self,
        tmp_req: btrip_open_20220520_models.ApplyExternalNodeStatusUpdateRequest,
        headers: btrip_open_20220520_models.ApplyExternalNodeStatusUpdateHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.ApplyExternalNodeStatusUpdateResponse:
        """
        @summary 外部审批节点状态同步
        
        @param tmp_req: ApplyExternalNodeStatusUpdateRequest
        @param headers: ApplyExternalNodeStatusUpdateHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: ApplyExternalNodeStatusUpdateResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.ApplyExternalNodeStatusUpdateShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.operation_records):
            request.operation_records_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.operation_records, 'operation_records', 'json')
        body = {}
        if not UtilClient.is_unset(request.node_id):
            body['node_id'] = request.node_id
        if not UtilClient.is_unset(request.operation_records_shrink):
            body['operation_records'] = request.operation_records_shrink
        if not UtilClient.is_unset(request.process_action_result):
            body['process_action_result'] = request.process_action_result
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='ApplyExternalNodeStatusUpdate',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/apply/v1/external-nodes/action/status-update',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.ApplyExternalNodeStatusUpdateResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def apply_external_node_status_update(
        self,
        request: btrip_open_20220520_models.ApplyExternalNodeStatusUpdateRequest,
    ) -> btrip_open_20220520_models.ApplyExternalNodeStatusUpdateResponse:
        """
        @summary 外部审批节点状态同步
        
        @param request: ApplyExternalNodeStatusUpdateRequest
        @return: ApplyExternalNodeStatusUpdateResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.ApplyExternalNodeStatusUpdateHeaders()
        return self.apply_external_node_status_update_with_options(request, headers, runtime)

    async def apply_external_node_status_update_async(
        self,
        request: btrip_open_20220520_models.ApplyExternalNodeStatusUpdateRequest,
    ) -> btrip_open_20220520_models.ApplyExternalNodeStatusUpdateResponse:
        """
        @summary 外部审批节点状态同步
        
        @param request: ApplyExternalNodeStatusUpdateRequest
        @return: ApplyExternalNodeStatusUpdateResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.ApplyExternalNodeStatusUpdateHeaders()
        return await self.apply_external_node_status_update_with_options_async(request, headers, runtime)

    def apply_invoice_task_with_options(
        self,
        tmp_req: btrip_open_20220520_models.ApplyInvoiceTaskRequest,
        headers: btrip_open_20220520_models.ApplyInvoiceTaskHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.ApplyInvoiceTaskResponse:
        """
        @summary 申请发票
        
        @param tmp_req: ApplyInvoiceTaskRequest
        @param headers: ApplyInvoiceTaskHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: ApplyInvoiceTaskResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.ApplyInvoiceTaskShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.invoice_task_list):
            request.invoice_task_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.invoice_task_list, 'invoice_task_list', 'json')
        body = {}
        if not UtilClient.is_unset(request.bill_date):
            body['bill_date'] = request.bill_date
        if not UtilClient.is_unset(request.invoice_task_list_shrink):
            body['invoice_task_list'] = request.invoice_task_list_shrink
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='ApplyInvoiceTask',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/invoice/v1/apply-invoice-task',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.ApplyInvoiceTaskResponse(),
            self.call_api(params, req, runtime)
        )

    async def apply_invoice_task_with_options_async(
        self,
        tmp_req: btrip_open_20220520_models.ApplyInvoiceTaskRequest,
        headers: btrip_open_20220520_models.ApplyInvoiceTaskHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.ApplyInvoiceTaskResponse:
        """
        @summary 申请发票
        
        @param tmp_req: ApplyInvoiceTaskRequest
        @param headers: ApplyInvoiceTaskHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: ApplyInvoiceTaskResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.ApplyInvoiceTaskShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.invoice_task_list):
            request.invoice_task_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.invoice_task_list, 'invoice_task_list', 'json')
        body = {}
        if not UtilClient.is_unset(request.bill_date):
            body['bill_date'] = request.bill_date
        if not UtilClient.is_unset(request.invoice_task_list_shrink):
            body['invoice_task_list'] = request.invoice_task_list_shrink
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='ApplyInvoiceTask',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/invoice/v1/apply-invoice-task',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.ApplyInvoiceTaskResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def apply_invoice_task(
        self,
        request: btrip_open_20220520_models.ApplyInvoiceTaskRequest,
    ) -> btrip_open_20220520_models.ApplyInvoiceTaskResponse:
        """
        @summary 申请发票
        
        @param request: ApplyInvoiceTaskRequest
        @return: ApplyInvoiceTaskResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.ApplyInvoiceTaskHeaders()
        return self.apply_invoice_task_with_options(request, headers, runtime)

    async def apply_invoice_task_async(
        self,
        request: btrip_open_20220520_models.ApplyInvoiceTaskRequest,
    ) -> btrip_open_20220520_models.ApplyInvoiceTaskResponse:
        """
        @summary 申请发票
        
        @param request: ApplyInvoiceTaskRequest
        @return: ApplyInvoiceTaskResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.ApplyInvoiceTaskHeaders()
        return await self.apply_invoice_task_with_options_async(request, headers, runtime)

    def apply_list_query_with_options(
        self,
        request: btrip_open_20220520_models.ApplyListQueryRequest,
        headers: btrip_open_20220520_models.ApplyListQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.ApplyListQueryResponse:
        """
        @summary 查询出差审批单列表
        
        @param request: ApplyListQueryRequest
        @param headers: ApplyListQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: ApplyListQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.all_apply):
            query['all_apply'] = request.all_apply
        if not UtilClient.is_unset(request.depart_id):
            query['depart_id'] = request.depart_id
        if not UtilClient.is_unset(request.end_time):
            query['end_time'] = request.end_time
        if not UtilClient.is_unset(request.gmt_modified):
            query['gmt_modified'] = request.gmt_modified
        if not UtilClient.is_unset(request.only_shang_lv_apply):
            query['only_shang_lv_apply'] = request.only_shang_lv_apply
        if not UtilClient.is_unset(request.page):
            query['page'] = request.page
        if not UtilClient.is_unset(request.page_size):
            query['page_size'] = request.page_size
        if not UtilClient.is_unset(request.start_time):
            query['start_time'] = request.start_time
        if not UtilClient.is_unset(request.sub_corp_id):
            query['sub_corp_id'] = request.sub_corp_id
        if not UtilClient.is_unset(request.type):
            query['type'] = request.type
        if not UtilClient.is_unset(request.union_no):
            query['union_no'] = request.union_no
        if not UtilClient.is_unset(request.user_id):
            query['user_id'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ApplyListQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/apply/v1/biz-trips',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.ApplyListQueryResponse(),
            self.call_api(params, req, runtime)
        )

    async def apply_list_query_with_options_async(
        self,
        request: btrip_open_20220520_models.ApplyListQueryRequest,
        headers: btrip_open_20220520_models.ApplyListQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.ApplyListQueryResponse:
        """
        @summary 查询出差审批单列表
        
        @param request: ApplyListQueryRequest
        @param headers: ApplyListQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: ApplyListQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.all_apply):
            query['all_apply'] = request.all_apply
        if not UtilClient.is_unset(request.depart_id):
            query['depart_id'] = request.depart_id
        if not UtilClient.is_unset(request.end_time):
            query['end_time'] = request.end_time
        if not UtilClient.is_unset(request.gmt_modified):
            query['gmt_modified'] = request.gmt_modified
        if not UtilClient.is_unset(request.only_shang_lv_apply):
            query['only_shang_lv_apply'] = request.only_shang_lv_apply
        if not UtilClient.is_unset(request.page):
            query['page'] = request.page
        if not UtilClient.is_unset(request.page_size):
            query['page_size'] = request.page_size
        if not UtilClient.is_unset(request.start_time):
            query['start_time'] = request.start_time
        if not UtilClient.is_unset(request.sub_corp_id):
            query['sub_corp_id'] = request.sub_corp_id
        if not UtilClient.is_unset(request.type):
            query['type'] = request.type
        if not UtilClient.is_unset(request.union_no):
            query['union_no'] = request.union_no
        if not UtilClient.is_unset(request.user_id):
            query['user_id'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ApplyListQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/apply/v1/biz-trips',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.ApplyListQueryResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def apply_list_query(
        self,
        request: btrip_open_20220520_models.ApplyListQueryRequest,
    ) -> btrip_open_20220520_models.ApplyListQueryResponse:
        """
        @summary 查询出差审批单列表
        
        @param request: ApplyListQueryRequest
        @return: ApplyListQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.ApplyListQueryHeaders()
        return self.apply_list_query_with_options(request, headers, runtime)

    async def apply_list_query_async(
        self,
        request: btrip_open_20220520_models.ApplyListQueryRequest,
    ) -> btrip_open_20220520_models.ApplyListQueryResponse:
        """
        @summary 查询出差审批单列表
        
        @param request: ApplyListQueryRequest
        @return: ApplyListQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.ApplyListQueryHeaders()
        return await self.apply_list_query_with_options_async(request, headers, runtime)

    def apply_modify_with_options(
        self,
        tmp_req: btrip_open_20220520_models.ApplyModifyRequest,
        headers: btrip_open_20220520_models.ApplyModifyHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.ApplyModifyResponse:
        """
        @summary 更新出差审批单
        
        @param tmp_req: ApplyModifyRequest
        @param headers: ApplyModifyHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: ApplyModifyResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.ApplyModifyShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.car_rule):
            request.car_rule_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.car_rule, 'car_rule', 'json')
        if not UtilClient.is_unset(tmp_req.external_traveler_list):
            request.external_traveler_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.external_traveler_list, 'external_traveler_list', 'json')
        if not UtilClient.is_unset(tmp_req.external_traveler_standard):
            request.external_traveler_standard_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.external_traveler_standard, 'external_traveler_standard', 'json')
        if not UtilClient.is_unset(tmp_req.hotel_share):
            request.hotel_share_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.hotel_share, 'hotel_share', 'json')
        if not UtilClient.is_unset(tmp_req.itinerary_list):
            request.itinerary_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.itinerary_list, 'itinerary_list', 'json')
        if not UtilClient.is_unset(tmp_req.itinerary_set_list):
            request.itinerary_set_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.itinerary_set_list, 'itinerary_set_list', 'json')
        if not UtilClient.is_unset(tmp_req.traveler_list):
            request.traveler_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.traveler_list, 'traveler_list', 'json')
        if not UtilClient.is_unset(tmp_req.traveler_standard):
            request.traveler_standard_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.traveler_standard, 'traveler_standard', 'json')
        body = {}
        if not UtilClient.is_unset(request.budget):
            body['budget'] = request.budget
        if not UtilClient.is_unset(request.budget_merge):
            body['budget_merge'] = request.budget_merge
        if not UtilClient.is_unset(request.car_rule_shrink):
            body['car_rule'] = request.car_rule_shrink
        if not UtilClient.is_unset(request.corp_name):
            body['corp_name'] = request.corp_name
        if not UtilClient.is_unset(request.depart_id):
            body['depart_id'] = request.depart_id
        if not UtilClient.is_unset(request.depart_name):
            body['depart_name'] = request.depart_name
        if not UtilClient.is_unset(request.extend_field):
            body['extend_field'] = request.extend_field
        if not UtilClient.is_unset(request.external_traveler_list_shrink):
            body['external_traveler_list'] = request.external_traveler_list_shrink
        if not UtilClient.is_unset(request.external_traveler_standard_shrink):
            body['external_traveler_standard'] = request.external_traveler_standard_shrink
        if not UtilClient.is_unset(request.flight_budget):
            body['flight_budget'] = request.flight_budget
        if not UtilClient.is_unset(request.hotel_budget):
            body['hotel_budget'] = request.hotel_budget
        if not UtilClient.is_unset(request.hotel_share_shrink):
            body['hotel_share'] = request.hotel_share_shrink
        if not UtilClient.is_unset(request.itinerary_list_shrink):
            body['itinerary_list'] = request.itinerary_list_shrink
        if not UtilClient.is_unset(request.itinerary_rule):
            body['itinerary_rule'] = request.itinerary_rule
        if not UtilClient.is_unset(request.itinerary_set_list_shrink):
            body['itinerary_set_list'] = request.itinerary_set_list_shrink
        if not UtilClient.is_unset(request.limit_traveler):
            body['limit_traveler'] = request.limit_traveler
        if not UtilClient.is_unset(request.payment_department_id):
            body['payment_department_id'] = request.payment_department_id
        if not UtilClient.is_unset(request.payment_department_name):
            body['payment_department_name'] = request.payment_department_name
        if not UtilClient.is_unset(request.status):
            body['status'] = request.status
        if not UtilClient.is_unset(request.sub_corp_id):
            body['sub_corp_id'] = request.sub_corp_id
        if not UtilClient.is_unset(request.thirdpart_apply_id):
            body['thirdpart_apply_id'] = request.thirdpart_apply_id
        if not UtilClient.is_unset(request.thirdpart_business_id):
            body['thirdpart_business_id'] = request.thirdpart_business_id
        if not UtilClient.is_unset(request.thirdpart_depart_id):
            body['thirdpart_depart_id'] = request.thirdpart_depart_id
        if not UtilClient.is_unset(request.together_book_rule):
            body['together_book_rule'] = request.together_book_rule
        if not UtilClient.is_unset(request.train_budget):
            body['train_budget'] = request.train_budget
        if not UtilClient.is_unset(request.traveler_list_shrink):
            body['traveler_list'] = request.traveler_list_shrink
        if not UtilClient.is_unset(request.traveler_standard_shrink):
            body['traveler_standard'] = request.traveler_standard_shrink
        if not UtilClient.is_unset(request.trip_cause):
            body['trip_cause'] = request.trip_cause
        if not UtilClient.is_unset(request.trip_day):
            body['trip_day'] = request.trip_day
        if not UtilClient.is_unset(request.trip_title):
            body['trip_title'] = request.trip_title
        if not UtilClient.is_unset(request.union_no):
            body['union_no'] = request.union_no
        if not UtilClient.is_unset(request.user_id):
            body['user_id'] = request.user_id
        if not UtilClient.is_unset(request.user_name):
            body['user_name'] = request.user_name
        if not UtilClient.is_unset(request.vehicle_budget):
            body['vehicle_budget'] = request.vehicle_budget
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='ApplyModify',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/apply/v1/biz-trip',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.ApplyModifyResponse(),
            self.call_api(params, req, runtime)
        )

    async def apply_modify_with_options_async(
        self,
        tmp_req: btrip_open_20220520_models.ApplyModifyRequest,
        headers: btrip_open_20220520_models.ApplyModifyHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.ApplyModifyResponse:
        """
        @summary 更新出差审批单
        
        @param tmp_req: ApplyModifyRequest
        @param headers: ApplyModifyHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: ApplyModifyResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.ApplyModifyShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.car_rule):
            request.car_rule_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.car_rule, 'car_rule', 'json')
        if not UtilClient.is_unset(tmp_req.external_traveler_list):
            request.external_traveler_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.external_traveler_list, 'external_traveler_list', 'json')
        if not UtilClient.is_unset(tmp_req.external_traveler_standard):
            request.external_traveler_standard_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.external_traveler_standard, 'external_traveler_standard', 'json')
        if not UtilClient.is_unset(tmp_req.hotel_share):
            request.hotel_share_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.hotel_share, 'hotel_share', 'json')
        if not UtilClient.is_unset(tmp_req.itinerary_list):
            request.itinerary_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.itinerary_list, 'itinerary_list', 'json')
        if not UtilClient.is_unset(tmp_req.itinerary_set_list):
            request.itinerary_set_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.itinerary_set_list, 'itinerary_set_list', 'json')
        if not UtilClient.is_unset(tmp_req.traveler_list):
            request.traveler_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.traveler_list, 'traveler_list', 'json')
        if not UtilClient.is_unset(tmp_req.traveler_standard):
            request.traveler_standard_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.traveler_standard, 'traveler_standard', 'json')
        body = {}
        if not UtilClient.is_unset(request.budget):
            body['budget'] = request.budget
        if not UtilClient.is_unset(request.budget_merge):
            body['budget_merge'] = request.budget_merge
        if not UtilClient.is_unset(request.car_rule_shrink):
            body['car_rule'] = request.car_rule_shrink
        if not UtilClient.is_unset(request.corp_name):
            body['corp_name'] = request.corp_name
        if not UtilClient.is_unset(request.depart_id):
            body['depart_id'] = request.depart_id
        if not UtilClient.is_unset(request.depart_name):
            body['depart_name'] = request.depart_name
        if not UtilClient.is_unset(request.extend_field):
            body['extend_field'] = request.extend_field
        if not UtilClient.is_unset(request.external_traveler_list_shrink):
            body['external_traveler_list'] = request.external_traveler_list_shrink
        if not UtilClient.is_unset(request.external_traveler_standard_shrink):
            body['external_traveler_standard'] = request.external_traveler_standard_shrink
        if not UtilClient.is_unset(request.flight_budget):
            body['flight_budget'] = request.flight_budget
        if not UtilClient.is_unset(request.hotel_budget):
            body['hotel_budget'] = request.hotel_budget
        if not UtilClient.is_unset(request.hotel_share_shrink):
            body['hotel_share'] = request.hotel_share_shrink
        if not UtilClient.is_unset(request.itinerary_list_shrink):
            body['itinerary_list'] = request.itinerary_list_shrink
        if not UtilClient.is_unset(request.itinerary_rule):
            body['itinerary_rule'] = request.itinerary_rule
        if not UtilClient.is_unset(request.itinerary_set_list_shrink):
            body['itinerary_set_list'] = request.itinerary_set_list_shrink
        if not UtilClient.is_unset(request.limit_traveler):
            body['limit_traveler'] = request.limit_traveler
        if not UtilClient.is_unset(request.payment_department_id):
            body['payment_department_id'] = request.payment_department_id
        if not UtilClient.is_unset(request.payment_department_name):
            body['payment_department_name'] = request.payment_department_name
        if not UtilClient.is_unset(request.status):
            body['status'] = request.status
        if not UtilClient.is_unset(request.sub_corp_id):
            body['sub_corp_id'] = request.sub_corp_id
        if not UtilClient.is_unset(request.thirdpart_apply_id):
            body['thirdpart_apply_id'] = request.thirdpart_apply_id
        if not UtilClient.is_unset(request.thirdpart_business_id):
            body['thirdpart_business_id'] = request.thirdpart_business_id
        if not UtilClient.is_unset(request.thirdpart_depart_id):
            body['thirdpart_depart_id'] = request.thirdpart_depart_id
        if not UtilClient.is_unset(request.together_book_rule):
            body['together_book_rule'] = request.together_book_rule
        if not UtilClient.is_unset(request.train_budget):
            body['train_budget'] = request.train_budget
        if not UtilClient.is_unset(request.traveler_list_shrink):
            body['traveler_list'] = request.traveler_list_shrink
        if not UtilClient.is_unset(request.traveler_standard_shrink):
            body['traveler_standard'] = request.traveler_standard_shrink
        if not UtilClient.is_unset(request.trip_cause):
            body['trip_cause'] = request.trip_cause
        if not UtilClient.is_unset(request.trip_day):
            body['trip_day'] = request.trip_day
        if not UtilClient.is_unset(request.trip_title):
            body['trip_title'] = request.trip_title
        if not UtilClient.is_unset(request.union_no):
            body['union_no'] = request.union_no
        if not UtilClient.is_unset(request.user_id):
            body['user_id'] = request.user_id
        if not UtilClient.is_unset(request.user_name):
            body['user_name'] = request.user_name
        if not UtilClient.is_unset(request.vehicle_budget):
            body['vehicle_budget'] = request.vehicle_budget
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='ApplyModify',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/apply/v1/biz-trip',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.ApplyModifyResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def apply_modify(
        self,
        request: btrip_open_20220520_models.ApplyModifyRequest,
    ) -> btrip_open_20220520_models.ApplyModifyResponse:
        """
        @summary 更新出差审批单
        
        @param request: ApplyModifyRequest
        @return: ApplyModifyResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.ApplyModifyHeaders()
        return self.apply_modify_with_options(request, headers, runtime)

    async def apply_modify_async(
        self,
        request: btrip_open_20220520_models.ApplyModifyRequest,
    ) -> btrip_open_20220520_models.ApplyModifyResponse:
        """
        @summary 更新出差审批单
        
        @param request: ApplyModifyRequest
        @return: ApplyModifyResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.ApplyModifyHeaders()
        return await self.apply_modify_with_options_async(request, headers, runtime)

    def apply_query_with_options(
        self,
        request: btrip_open_20220520_models.ApplyQueryRequest,
        headers: btrip_open_20220520_models.ApplyQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.ApplyQueryResponse:
        """
        @summary 查询出差审批单详情
        
        @param request: ApplyQueryRequest
        @param headers: ApplyQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: ApplyQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.apply_id):
            query['apply_id'] = request.apply_id
        if not UtilClient.is_unset(request.apply_show_id):
            query['apply_show_id'] = request.apply_show_id
        if not UtilClient.is_unset(request.sub_corp_id):
            query['sub_corp_id'] = request.sub_corp_id
        if not UtilClient.is_unset(request.thirdpart_apply_id):
            query['thirdpart_apply_id'] = request.thirdpart_apply_id
        if not UtilClient.is_unset(request.type):
            query['type'] = request.type
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ApplyQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/apply/v1/biz-trip',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.ApplyQueryResponse(),
            self.call_api(params, req, runtime)
        )

    async def apply_query_with_options_async(
        self,
        request: btrip_open_20220520_models.ApplyQueryRequest,
        headers: btrip_open_20220520_models.ApplyQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.ApplyQueryResponse:
        """
        @summary 查询出差审批单详情
        
        @param request: ApplyQueryRequest
        @param headers: ApplyQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: ApplyQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.apply_id):
            query['apply_id'] = request.apply_id
        if not UtilClient.is_unset(request.apply_show_id):
            query['apply_show_id'] = request.apply_show_id
        if not UtilClient.is_unset(request.sub_corp_id):
            query['sub_corp_id'] = request.sub_corp_id
        if not UtilClient.is_unset(request.thirdpart_apply_id):
            query['thirdpart_apply_id'] = request.thirdpart_apply_id
        if not UtilClient.is_unset(request.type):
            query['type'] = request.type
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ApplyQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/apply/v1/biz-trip',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.ApplyQueryResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def apply_query(
        self,
        request: btrip_open_20220520_models.ApplyQueryRequest,
    ) -> btrip_open_20220520_models.ApplyQueryResponse:
        """
        @summary 查询出差审批单详情
        
        @param request: ApplyQueryRequest
        @return: ApplyQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.ApplyQueryHeaders()
        return self.apply_query_with_options(request, headers, runtime)

    async def apply_query_async(
        self,
        request: btrip_open_20220520_models.ApplyQueryRequest,
    ) -> btrip_open_20220520_models.ApplyQueryResponse:
        """
        @summary 查询出差审批单详情
        
        @param request: ApplyQueryRequest
        @return: ApplyQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.ApplyQueryHeaders()
        return await self.apply_query_with_options_async(request, headers, runtime)

    def base_city_info_search_with_options(
        self,
        request: btrip_open_20220520_models.BaseCityInfoSearchRequest,
        headers: btrip_open_20220520_models.BaseCityInfoSearchHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.BaseCityInfoSearchResponse:
        """
        @summary 搜索国内/国际（港澳台）城市基础行政区划数据
        
        @param request: BaseCityInfoSearchRequest
        @param headers: BaseCityInfoSearchHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: BaseCityInfoSearchResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.keyword):
            query['keyword'] = request.keyword
        if not UtilClient.is_unset(request.region):
            query['region'] = request.region
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_access_token):
            real_headers['x-acs-btrip-access-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='BaseCityInfoSearch',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/city/v1/cities/action/search',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.BaseCityInfoSearchResponse(),
            self.call_api(params, req, runtime)
        )

    async def base_city_info_search_with_options_async(
        self,
        request: btrip_open_20220520_models.BaseCityInfoSearchRequest,
        headers: btrip_open_20220520_models.BaseCityInfoSearchHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.BaseCityInfoSearchResponse:
        """
        @summary 搜索国内/国际（港澳台）城市基础行政区划数据
        
        @param request: BaseCityInfoSearchRequest
        @param headers: BaseCityInfoSearchHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: BaseCityInfoSearchResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.keyword):
            query['keyword'] = request.keyword
        if not UtilClient.is_unset(request.region):
            query['region'] = request.region
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_access_token):
            real_headers['x-acs-btrip-access-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='BaseCityInfoSearch',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/city/v1/cities/action/search',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.BaseCityInfoSearchResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def base_city_info_search(
        self,
        request: btrip_open_20220520_models.BaseCityInfoSearchRequest,
    ) -> btrip_open_20220520_models.BaseCityInfoSearchResponse:
        """
        @summary 搜索国内/国际（港澳台）城市基础行政区划数据
        
        @param request: BaseCityInfoSearchRequest
        @return: BaseCityInfoSearchResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.BaseCityInfoSearchHeaders()
        return self.base_city_info_search_with_options(request, headers, runtime)

    async def base_city_info_search_async(
        self,
        request: btrip_open_20220520_models.BaseCityInfoSearchRequest,
    ) -> btrip_open_20220520_models.BaseCityInfoSearchResponse:
        """
        @summary 搜索国内/国际（港澳台）城市基础行政区划数据
        
        @param request: BaseCityInfoSearchRequest
        @return: BaseCityInfoSearchResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.BaseCityInfoSearchHeaders()
        return await self.base_city_info_search_with_options_async(request, headers, runtime)

    def btrip_bill_info_adjust_with_options(
        self,
        request: btrip_open_20220520_models.BtripBillInfoAdjustRequest,
        headers: btrip_open_20220520_models.BtripBillInfoAdjustHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.BtripBillInfoAdjustResponse:
        """
        @summary 商旅账单内容修改
        
        @param request: BtripBillInfoAdjustRequest
        @param headers: BtripBillInfoAdjustHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: BtripBillInfoAdjustResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.primary_id):
            body['primary_id'] = request.primary_id
        if not UtilClient.is_unset(request.third_part_cost_center_id):
            body['third_part_cost_center_id'] = request.third_part_cost_center_id
        if not UtilClient.is_unset(request.third_part_department_id):
            body['third_part_department_id'] = request.third_part_department_id
        if not UtilClient.is_unset(request.third_part_invoice_id):
            body['third_part_invoice_id'] = request.third_part_invoice_id
        if not UtilClient.is_unset(request.third_part_project_id):
            body['third_part_project_id'] = request.third_part_project_id
        if not UtilClient.is_unset(request.user_id):
            body['user_id'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='BtripBillInfoAdjust',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/bill/v1/info/action/adjust',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.BtripBillInfoAdjustResponse(),
            self.call_api(params, req, runtime)
        )

    async def btrip_bill_info_adjust_with_options_async(
        self,
        request: btrip_open_20220520_models.BtripBillInfoAdjustRequest,
        headers: btrip_open_20220520_models.BtripBillInfoAdjustHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.BtripBillInfoAdjustResponse:
        """
        @summary 商旅账单内容修改
        
        @param request: BtripBillInfoAdjustRequest
        @param headers: BtripBillInfoAdjustHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: BtripBillInfoAdjustResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.primary_id):
            body['primary_id'] = request.primary_id
        if not UtilClient.is_unset(request.third_part_cost_center_id):
            body['third_part_cost_center_id'] = request.third_part_cost_center_id
        if not UtilClient.is_unset(request.third_part_department_id):
            body['third_part_department_id'] = request.third_part_department_id
        if not UtilClient.is_unset(request.third_part_invoice_id):
            body['third_part_invoice_id'] = request.third_part_invoice_id
        if not UtilClient.is_unset(request.third_part_project_id):
            body['third_part_project_id'] = request.third_part_project_id
        if not UtilClient.is_unset(request.user_id):
            body['user_id'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='BtripBillInfoAdjust',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/bill/v1/info/action/adjust',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.BtripBillInfoAdjustResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def btrip_bill_info_adjust(
        self,
        request: btrip_open_20220520_models.BtripBillInfoAdjustRequest,
    ) -> btrip_open_20220520_models.BtripBillInfoAdjustResponse:
        """
        @summary 商旅账单内容修改
        
        @param request: BtripBillInfoAdjustRequest
        @return: BtripBillInfoAdjustResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.BtripBillInfoAdjustHeaders()
        return self.btrip_bill_info_adjust_with_options(request, headers, runtime)

    async def btrip_bill_info_adjust_async(
        self,
        request: btrip_open_20220520_models.BtripBillInfoAdjustRequest,
    ) -> btrip_open_20220520_models.BtripBillInfoAdjustResponse:
        """
        @summary 商旅账单内容修改
        
        @param request: BtripBillInfoAdjustRequest
        @return: BtripBillInfoAdjustResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.BtripBillInfoAdjustHeaders()
        return await self.btrip_bill_info_adjust_with_options_async(request, headers, runtime)

    def car_apply_add_with_options(
        self,
        tmp_req: btrip_open_20220520_models.CarApplyAddRequest,
        headers: btrip_open_20220520_models.CarApplyAddHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.CarApplyAddResponse:
        """
        @summary 同步市内用车审批单
        
        @param tmp_req: CarApplyAddRequest
        @param headers: CarApplyAddHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: CarApplyAddResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.CarApplyAddShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.traveler_standard):
            request.traveler_standard_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.traveler_standard, 'traveler_standard', 'json')
        body = {}
        if not UtilClient.is_unset(request.cause):
            body['cause'] = request.cause
        if not UtilClient.is_unset(request.city):
            body['city'] = request.city
        if not UtilClient.is_unset(request.city_code_set):
            body['city_code_set'] = request.city_code_set
        if not UtilClient.is_unset(request.date):
            body['date'] = request.date
        if not UtilClient.is_unset(request.finished_date):
            body['finished_date'] = request.finished_date
        if not UtilClient.is_unset(request.project_code):
            body['project_code'] = request.project_code
        if not UtilClient.is_unset(request.project_name):
            body['project_name'] = request.project_name
        if not UtilClient.is_unset(request.status):
            body['status'] = request.status
        if not UtilClient.is_unset(request.third_part_apply_id):
            body['third_part_apply_id'] = request.third_part_apply_id
        if not UtilClient.is_unset(request.third_part_cost_center_id):
            body['third_part_cost_center_id'] = request.third_part_cost_center_id
        if not UtilClient.is_unset(request.third_part_invoice_id):
            body['third_part_invoice_id'] = request.third_part_invoice_id
        if not UtilClient.is_unset(request.times_total):
            body['times_total'] = request.times_total
        if not UtilClient.is_unset(request.times_type):
            body['times_type'] = request.times_type
        if not UtilClient.is_unset(request.times_used):
            body['times_used'] = request.times_used
        if not UtilClient.is_unset(request.title):
            body['title'] = request.title
        if not UtilClient.is_unset(request.traveler_standard_shrink):
            body['traveler_standard'] = request.traveler_standard_shrink
        if not UtilClient.is_unset(request.user_id):
            body['user_id'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CarApplyAdd',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/apply/v1/car',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.CarApplyAddResponse(),
            self.call_api(params, req, runtime)
        )

    async def car_apply_add_with_options_async(
        self,
        tmp_req: btrip_open_20220520_models.CarApplyAddRequest,
        headers: btrip_open_20220520_models.CarApplyAddHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.CarApplyAddResponse:
        """
        @summary 同步市内用车审批单
        
        @param tmp_req: CarApplyAddRequest
        @param headers: CarApplyAddHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: CarApplyAddResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.CarApplyAddShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.traveler_standard):
            request.traveler_standard_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.traveler_standard, 'traveler_standard', 'json')
        body = {}
        if not UtilClient.is_unset(request.cause):
            body['cause'] = request.cause
        if not UtilClient.is_unset(request.city):
            body['city'] = request.city
        if not UtilClient.is_unset(request.city_code_set):
            body['city_code_set'] = request.city_code_set
        if not UtilClient.is_unset(request.date):
            body['date'] = request.date
        if not UtilClient.is_unset(request.finished_date):
            body['finished_date'] = request.finished_date
        if not UtilClient.is_unset(request.project_code):
            body['project_code'] = request.project_code
        if not UtilClient.is_unset(request.project_name):
            body['project_name'] = request.project_name
        if not UtilClient.is_unset(request.status):
            body['status'] = request.status
        if not UtilClient.is_unset(request.third_part_apply_id):
            body['third_part_apply_id'] = request.third_part_apply_id
        if not UtilClient.is_unset(request.third_part_cost_center_id):
            body['third_part_cost_center_id'] = request.third_part_cost_center_id
        if not UtilClient.is_unset(request.third_part_invoice_id):
            body['third_part_invoice_id'] = request.third_part_invoice_id
        if not UtilClient.is_unset(request.times_total):
            body['times_total'] = request.times_total
        if not UtilClient.is_unset(request.times_type):
            body['times_type'] = request.times_type
        if not UtilClient.is_unset(request.times_used):
            body['times_used'] = request.times_used
        if not UtilClient.is_unset(request.title):
            body['title'] = request.title
        if not UtilClient.is_unset(request.traveler_standard_shrink):
            body['traveler_standard'] = request.traveler_standard_shrink
        if not UtilClient.is_unset(request.user_id):
            body['user_id'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CarApplyAdd',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/apply/v1/car',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.CarApplyAddResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def car_apply_add(
        self,
        request: btrip_open_20220520_models.CarApplyAddRequest,
    ) -> btrip_open_20220520_models.CarApplyAddResponse:
        """
        @summary 同步市内用车审批单
        
        @param request: CarApplyAddRequest
        @return: CarApplyAddResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.CarApplyAddHeaders()
        return self.car_apply_add_with_options(request, headers, runtime)

    async def car_apply_add_async(
        self,
        request: btrip_open_20220520_models.CarApplyAddRequest,
    ) -> btrip_open_20220520_models.CarApplyAddResponse:
        """
        @summary 同步市内用车审批单
        
        @param request: CarApplyAddRequest
        @return: CarApplyAddResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.CarApplyAddHeaders()
        return await self.car_apply_add_with_options_async(request, headers, runtime)

    def car_apply_modify_with_options(
        self,
        request: btrip_open_20220520_models.CarApplyModifyRequest,
        headers: btrip_open_20220520_models.CarApplyModifyHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.CarApplyModifyResponse:
        """
        @summary 更新市内用车审批单
        
        @param request: CarApplyModifyRequest
        @param headers: CarApplyModifyHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: CarApplyModifyResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.operate_time):
            body['operate_time'] = request.operate_time
        if not UtilClient.is_unset(request.remark):
            body['remark'] = request.remark
        if not UtilClient.is_unset(request.status):
            body['status'] = request.status
        if not UtilClient.is_unset(request.third_part_apply_id):
            body['third_part_apply_id'] = request.third_part_apply_id
        if not UtilClient.is_unset(request.user_id):
            body['user_id'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CarApplyModify',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/apply/v1/car',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.CarApplyModifyResponse(),
            self.call_api(params, req, runtime)
        )

    async def car_apply_modify_with_options_async(
        self,
        request: btrip_open_20220520_models.CarApplyModifyRequest,
        headers: btrip_open_20220520_models.CarApplyModifyHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.CarApplyModifyResponse:
        """
        @summary 更新市内用车审批单
        
        @param request: CarApplyModifyRequest
        @param headers: CarApplyModifyHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: CarApplyModifyResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.operate_time):
            body['operate_time'] = request.operate_time
        if not UtilClient.is_unset(request.remark):
            body['remark'] = request.remark
        if not UtilClient.is_unset(request.status):
            body['status'] = request.status
        if not UtilClient.is_unset(request.third_part_apply_id):
            body['third_part_apply_id'] = request.third_part_apply_id
        if not UtilClient.is_unset(request.user_id):
            body['user_id'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CarApplyModify',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/apply/v1/car',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.CarApplyModifyResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def car_apply_modify(
        self,
        request: btrip_open_20220520_models.CarApplyModifyRequest,
    ) -> btrip_open_20220520_models.CarApplyModifyResponse:
        """
        @summary 更新市内用车审批单
        
        @param request: CarApplyModifyRequest
        @return: CarApplyModifyResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.CarApplyModifyHeaders()
        return self.car_apply_modify_with_options(request, headers, runtime)

    async def car_apply_modify_async(
        self,
        request: btrip_open_20220520_models.CarApplyModifyRequest,
    ) -> btrip_open_20220520_models.CarApplyModifyResponse:
        """
        @summary 更新市内用车审批单
        
        @param request: CarApplyModifyRequest
        @return: CarApplyModifyResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.CarApplyModifyHeaders()
        return await self.car_apply_modify_with_options_async(request, headers, runtime)

    def car_apply_query_with_options(
        self,
        request: btrip_open_20220520_models.CarApplyQueryRequest,
        headers: btrip_open_20220520_models.CarApplyQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.CarApplyQueryResponse:
        """
        @summary 查询市内用车审批单
        
        @param request: CarApplyQueryRequest
        @param headers: CarApplyQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: CarApplyQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.created_end_at):
            query['created_end_at'] = request.created_end_at
        if not UtilClient.is_unset(request.created_start_at):
            query['created_start_at'] = request.created_start_at
        if not UtilClient.is_unset(request.page_number):
            query['page_number'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['page_size'] = request.page_size
        if not UtilClient.is_unset(request.third_part_apply_id):
            query['third_part_apply_id'] = request.third_part_apply_id
        if not UtilClient.is_unset(request.user_id):
            query['user_id'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CarApplyQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/apply/v1/car',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.CarApplyQueryResponse(),
            self.call_api(params, req, runtime)
        )

    async def car_apply_query_with_options_async(
        self,
        request: btrip_open_20220520_models.CarApplyQueryRequest,
        headers: btrip_open_20220520_models.CarApplyQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.CarApplyQueryResponse:
        """
        @summary 查询市内用车审批单
        
        @param request: CarApplyQueryRequest
        @param headers: CarApplyQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: CarApplyQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.created_end_at):
            query['created_end_at'] = request.created_end_at
        if not UtilClient.is_unset(request.created_start_at):
            query['created_start_at'] = request.created_start_at
        if not UtilClient.is_unset(request.page_number):
            query['page_number'] = request.page_number
        if not UtilClient.is_unset(request.page_size):
            query['page_size'] = request.page_size
        if not UtilClient.is_unset(request.third_part_apply_id):
            query['third_part_apply_id'] = request.third_part_apply_id
        if not UtilClient.is_unset(request.user_id):
            query['user_id'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CarApplyQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/apply/v1/car',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.CarApplyQueryResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def car_apply_query(
        self,
        request: btrip_open_20220520_models.CarApplyQueryRequest,
    ) -> btrip_open_20220520_models.CarApplyQueryResponse:
        """
        @summary 查询市内用车审批单
        
        @param request: CarApplyQueryRequest
        @return: CarApplyQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.CarApplyQueryHeaders()
        return self.car_apply_query_with_options(request, headers, runtime)

    async def car_apply_query_async(
        self,
        request: btrip_open_20220520_models.CarApplyQueryRequest,
    ) -> btrip_open_20220520_models.CarApplyQueryResponse:
        """
        @summary 查询市内用车审批单
        
        @param request: CarApplyQueryRequest
        @return: CarApplyQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.CarApplyQueryHeaders()
        return await self.car_apply_query_with_options_async(request, headers, runtime)

    def car_bill_settlement_query_with_options(
        self,
        request: btrip_open_20220520_models.CarBillSettlementQueryRequest,
        headers: btrip_open_20220520_models.CarBillSettlementQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.CarBillSettlementQueryResponse:
        """
        @summary 查询用车记账数据
        
        @param request: CarBillSettlementQueryRequest
        @param headers: CarBillSettlementQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: CarBillSettlementQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.page_no):
            query['page_no'] = request.page_no
        if not UtilClient.is_unset(request.page_size):
            query['page_size'] = request.page_size
        if not UtilClient.is_unset(request.period_end):
            query['period_end'] = request.period_end
        if not UtilClient.is_unset(request.period_start):
            query['period_start'] = request.period_start
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CarBillSettlementQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/car/v1/bill-settlement',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.CarBillSettlementQueryResponse(),
            self.call_api(params, req, runtime)
        )

    async def car_bill_settlement_query_with_options_async(
        self,
        request: btrip_open_20220520_models.CarBillSettlementQueryRequest,
        headers: btrip_open_20220520_models.CarBillSettlementQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.CarBillSettlementQueryResponse:
        """
        @summary 查询用车记账数据
        
        @param request: CarBillSettlementQueryRequest
        @param headers: CarBillSettlementQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: CarBillSettlementQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.page_no):
            query['page_no'] = request.page_no
        if not UtilClient.is_unset(request.page_size):
            query['page_size'] = request.page_size
        if not UtilClient.is_unset(request.period_end):
            query['period_end'] = request.period_end
        if not UtilClient.is_unset(request.period_start):
            query['period_start'] = request.period_start
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CarBillSettlementQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/car/v1/bill-settlement',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.CarBillSettlementQueryResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def car_bill_settlement_query(
        self,
        request: btrip_open_20220520_models.CarBillSettlementQueryRequest,
    ) -> btrip_open_20220520_models.CarBillSettlementQueryResponse:
        """
        @summary 查询用车记账数据
        
        @param request: CarBillSettlementQueryRequest
        @return: CarBillSettlementQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.CarBillSettlementQueryHeaders()
        return self.car_bill_settlement_query_with_options(request, headers, runtime)

    async def car_bill_settlement_query_async(
        self,
        request: btrip_open_20220520_models.CarBillSettlementQueryRequest,
    ) -> btrip_open_20220520_models.CarBillSettlementQueryResponse:
        """
        @summary 查询用车记账数据
        
        @param request: CarBillSettlementQueryRequest
        @return: CarBillSettlementQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.CarBillSettlementQueryHeaders()
        return await self.car_bill_settlement_query_with_options_async(request, headers, runtime)

    def car_order_list_query_with_options(
        self,
        request: btrip_open_20220520_models.CarOrderListQueryRequest,
        headers: btrip_open_20220520_models.CarOrderListQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.CarOrderListQueryResponse:
        """
        @summary 查询用车订单列表
        
        @param request: CarOrderListQueryRequest
        @param headers: CarOrderListQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: CarOrderListQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.all_apply):
            query['all_apply'] = request.all_apply
        if not UtilClient.is_unset(request.apply_id):
            query['apply_id'] = request.apply_id
        if not UtilClient.is_unset(request.depart_id):
            query['depart_id'] = request.depart_id
        if not UtilClient.is_unset(request.end_time):
            query['end_time'] = request.end_time
        if not UtilClient.is_unset(request.page):
            query['page'] = request.page
        if not UtilClient.is_unset(request.page_size):
            query['page_size'] = request.page_size
        if not UtilClient.is_unset(request.start_time):
            query['start_time'] = request.start_time
        if not UtilClient.is_unset(request.thirdpart_apply_id):
            query['thirdpart_apply_id'] = request.thirdpart_apply_id
        if not UtilClient.is_unset(request.update_end_time):
            query['update_end_time'] = request.update_end_time
        if not UtilClient.is_unset(request.update_start_time):
            query['update_start_time'] = request.update_start_time
        if not UtilClient.is_unset(request.user_id):
            query['user_id'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CarOrderListQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/car/v1/order-list',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.CarOrderListQueryResponse(),
            self.call_api(params, req, runtime)
        )

    async def car_order_list_query_with_options_async(
        self,
        request: btrip_open_20220520_models.CarOrderListQueryRequest,
        headers: btrip_open_20220520_models.CarOrderListQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.CarOrderListQueryResponse:
        """
        @summary 查询用车订单列表
        
        @param request: CarOrderListQueryRequest
        @param headers: CarOrderListQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: CarOrderListQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.all_apply):
            query['all_apply'] = request.all_apply
        if not UtilClient.is_unset(request.apply_id):
            query['apply_id'] = request.apply_id
        if not UtilClient.is_unset(request.depart_id):
            query['depart_id'] = request.depart_id
        if not UtilClient.is_unset(request.end_time):
            query['end_time'] = request.end_time
        if not UtilClient.is_unset(request.page):
            query['page'] = request.page
        if not UtilClient.is_unset(request.page_size):
            query['page_size'] = request.page_size
        if not UtilClient.is_unset(request.start_time):
            query['start_time'] = request.start_time
        if not UtilClient.is_unset(request.thirdpart_apply_id):
            query['thirdpart_apply_id'] = request.thirdpart_apply_id
        if not UtilClient.is_unset(request.update_end_time):
            query['update_end_time'] = request.update_end_time
        if not UtilClient.is_unset(request.update_start_time):
            query['update_start_time'] = request.update_start_time
        if not UtilClient.is_unset(request.user_id):
            query['user_id'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CarOrderListQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/car/v1/order-list',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.CarOrderListQueryResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def car_order_list_query(
        self,
        request: btrip_open_20220520_models.CarOrderListQueryRequest,
    ) -> btrip_open_20220520_models.CarOrderListQueryResponse:
        """
        @summary 查询用车订单列表
        
        @param request: CarOrderListQueryRequest
        @return: CarOrderListQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.CarOrderListQueryHeaders()
        return self.car_order_list_query_with_options(request, headers, runtime)

    async def car_order_list_query_async(
        self,
        request: btrip_open_20220520_models.CarOrderListQueryRequest,
    ) -> btrip_open_20220520_models.CarOrderListQueryResponse:
        """
        @summary 查询用车订单列表
        
        @param request: CarOrderListQueryRequest
        @return: CarOrderListQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.CarOrderListQueryHeaders()
        return await self.car_order_list_query_with_options_async(request, headers, runtime)

    def car_order_query_with_options(
        self,
        request: btrip_open_20220520_models.CarOrderQueryRequest,
        headers: btrip_open_20220520_models.CarOrderQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.CarOrderQueryResponse:
        """
        @summary 用车订单查询
        
        @param request: CarOrderQueryRequest
        @param headers: CarOrderQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: CarOrderQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.order_id):
            query['order_id'] = request.order_id
        if not UtilClient.is_unset(request.sub_order_id):
            query['sub_order_id'] = request.sub_order_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CarOrderQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/car/v1/order',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.CarOrderQueryResponse(),
            self.call_api(params, req, runtime)
        )

    async def car_order_query_with_options_async(
        self,
        request: btrip_open_20220520_models.CarOrderQueryRequest,
        headers: btrip_open_20220520_models.CarOrderQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.CarOrderQueryResponse:
        """
        @summary 用车订单查询
        
        @param request: CarOrderQueryRequest
        @param headers: CarOrderQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: CarOrderQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.order_id):
            query['order_id'] = request.order_id
        if not UtilClient.is_unset(request.sub_order_id):
            query['sub_order_id'] = request.sub_order_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CarOrderQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/car/v1/order',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.CarOrderQueryResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def car_order_query(
        self,
        request: btrip_open_20220520_models.CarOrderQueryRequest,
    ) -> btrip_open_20220520_models.CarOrderQueryResponse:
        """
        @summary 用车订单查询
        
        @param request: CarOrderQueryRequest
        @return: CarOrderQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.CarOrderQueryHeaders()
        return self.car_order_query_with_options(request, headers, runtime)

    async def car_order_query_async(
        self,
        request: btrip_open_20220520_models.CarOrderQueryRequest,
    ) -> btrip_open_20220520_models.CarOrderQueryResponse:
        """
        @summary 用车订单查询
        
        @param request: CarOrderQueryRequest
        @return: CarOrderQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.CarOrderQueryHeaders()
        return await self.car_order_query_with_options_async(request, headers, runtime)

    def car_scene_query_with_options(
        self,
        headers: btrip_open_20220520_models.CarSceneQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.CarSceneQueryResponse:
        """
        @summary 查询企业用车场景
        
        @param headers: CarSceneQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: CarSceneQueryResponse
        """
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers
        )
        params = open_api_models.Params(
            action='CarSceneQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/car/v1/scenes',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.CarSceneQueryResponse(),
            self.call_api(params, req, runtime)
        )

    async def car_scene_query_with_options_async(
        self,
        headers: btrip_open_20220520_models.CarSceneQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.CarSceneQueryResponse:
        """
        @summary 查询企业用车场景
        
        @param headers: CarSceneQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: CarSceneQueryResponse
        """
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers
        )
        params = open_api_models.Params(
            action='CarSceneQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/car/v1/scenes',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.CarSceneQueryResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def car_scene_query(self) -> btrip_open_20220520_models.CarSceneQueryResponse:
        """
        @summary 查询企业用车场景
        
        @return: CarSceneQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.CarSceneQueryHeaders()
        return self.car_scene_query_with_options(headers, runtime)

    async def car_scene_query_async(self) -> btrip_open_20220520_models.CarSceneQueryResponse:
        """
        @summary 查询企业用车场景
        
        @return: CarSceneQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.CarSceneQueryHeaders()
        return await self.car_scene_query_with_options_async(headers, runtime)

    def city_search_with_options(
        self,
        request: btrip_open_20220520_models.CitySearchRequest,
        headers: btrip_open_20220520_models.CitySearchHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.CitySearchResponse:
        """
        @summary 查询行政区划（市，区）基础数据
        
        @param request: CitySearchRequest
        @param headers: CitySearchHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: CitySearchResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.keyword):
            query['keyword'] = request.keyword
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CitySearch',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/city/v1/city',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.CitySearchResponse(),
            self.call_api(params, req, runtime)
        )

    async def city_search_with_options_async(
        self,
        request: btrip_open_20220520_models.CitySearchRequest,
        headers: btrip_open_20220520_models.CitySearchHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.CitySearchResponse:
        """
        @summary 查询行政区划（市，区）基础数据
        
        @param request: CitySearchRequest
        @param headers: CitySearchHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: CitySearchResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.keyword):
            query['keyword'] = request.keyword
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CitySearch',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/city/v1/city',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.CitySearchResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def city_search(
        self,
        request: btrip_open_20220520_models.CitySearchRequest,
    ) -> btrip_open_20220520_models.CitySearchResponse:
        """
        @summary 查询行政区划（市，区）基础数据
        
        @param request: CitySearchRequest
        @return: CitySearchResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.CitySearchHeaders()
        return self.city_search_with_options(request, headers, runtime)

    async def city_search_async(
        self,
        request: btrip_open_20220520_models.CitySearchRequest,
    ) -> btrip_open_20220520_models.CitySearchResponse:
        """
        @summary 查询行政区划（市，区）基础数据
        
        @param request: CitySearchRequest
        @return: CitySearchResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.CitySearchHeaders()
        return await self.city_search_with_options_async(request, headers, runtime)

    def common_apply_query_with_options(
        self,
        request: btrip_open_20220520_models.CommonApplyQueryRequest,
        headers: btrip_open_20220520_models.CommonApplyQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.CommonApplyQueryResponse:
        """
        @summary 查询退改审批信息
        
        @param request: CommonApplyQueryRequest
        @param headers: CommonApplyQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: CommonApplyQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.apply_id):
            query['apply_id'] = request.apply_id
        if not UtilClient.is_unset(request.biz_category):
            query['biz_category'] = request.biz_category
        if not UtilClient.is_unset(request.user_id):
            query['user_id'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CommonApplyQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/apply/v1/common',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.CommonApplyQueryResponse(),
            self.call_api(params, req, runtime)
        )

    async def common_apply_query_with_options_async(
        self,
        request: btrip_open_20220520_models.CommonApplyQueryRequest,
        headers: btrip_open_20220520_models.CommonApplyQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.CommonApplyQueryResponse:
        """
        @summary 查询退改审批信息
        
        @param request: CommonApplyQueryRequest
        @param headers: CommonApplyQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: CommonApplyQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.apply_id):
            query['apply_id'] = request.apply_id
        if not UtilClient.is_unset(request.biz_category):
            query['biz_category'] = request.biz_category
        if not UtilClient.is_unset(request.user_id):
            query['user_id'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CommonApplyQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/apply/v1/common',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.CommonApplyQueryResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def common_apply_query(
        self,
        request: btrip_open_20220520_models.CommonApplyQueryRequest,
    ) -> btrip_open_20220520_models.CommonApplyQueryResponse:
        """
        @summary 查询退改审批信息
        
        @param request: CommonApplyQueryRequest
        @return: CommonApplyQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.CommonApplyQueryHeaders()
        return self.common_apply_query_with_options(request, headers, runtime)

    async def common_apply_query_async(
        self,
        request: btrip_open_20220520_models.CommonApplyQueryRequest,
    ) -> btrip_open_20220520_models.CommonApplyQueryResponse:
        """
        @summary 查询退改审批信息
        
        @param request: CommonApplyQueryRequest
        @return: CommonApplyQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.CommonApplyQueryHeaders()
        return await self.common_apply_query_with_options_async(request, headers, runtime)

    def common_apply_sync_with_options(
        self,
        request: btrip_open_20220520_models.CommonApplySyncRequest,
        headers: btrip_open_20220520_models.CommonApplySyncHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.CommonApplySyncResponse:
        """
        @summary 退改审批结果同步
        
        @param request: CommonApplySyncRequest
        @param headers: CommonApplySyncHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: CommonApplySyncResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.apply_id):
            query['apply_id'] = request.apply_id
        if not UtilClient.is_unset(request.biz_category):
            query['biz_category'] = request.biz_category
        if not UtilClient.is_unset(request.remark):
            query['remark'] = request.remark
        if not UtilClient.is_unset(request.status):
            query['status'] = request.status
        if not UtilClient.is_unset(request.thirdparty_flow_id):
            query['thirdparty_flow_id'] = request.thirdparty_flow_id
        if not UtilClient.is_unset(request.user_id):
            query['user_id'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CommonApplySync',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/apply/v1/syn-common',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.CommonApplySyncResponse(),
            self.call_api(params, req, runtime)
        )

    async def common_apply_sync_with_options_async(
        self,
        request: btrip_open_20220520_models.CommonApplySyncRequest,
        headers: btrip_open_20220520_models.CommonApplySyncHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.CommonApplySyncResponse:
        """
        @summary 退改审批结果同步
        
        @param request: CommonApplySyncRequest
        @param headers: CommonApplySyncHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: CommonApplySyncResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.apply_id):
            query['apply_id'] = request.apply_id
        if not UtilClient.is_unset(request.biz_category):
            query['biz_category'] = request.biz_category
        if not UtilClient.is_unset(request.remark):
            query['remark'] = request.remark
        if not UtilClient.is_unset(request.status):
            query['status'] = request.status
        if not UtilClient.is_unset(request.thirdparty_flow_id):
            query['thirdparty_flow_id'] = request.thirdparty_flow_id
        if not UtilClient.is_unset(request.user_id):
            query['user_id'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CommonApplySync',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/apply/v1/syn-common',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.CommonApplySyncResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def common_apply_sync(
        self,
        request: btrip_open_20220520_models.CommonApplySyncRequest,
    ) -> btrip_open_20220520_models.CommonApplySyncResponse:
        """
        @summary 退改审批结果同步
        
        @param request: CommonApplySyncRequest
        @return: CommonApplySyncResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.CommonApplySyncHeaders()
        return self.common_apply_sync_with_options(request, headers, runtime)

    async def common_apply_sync_async(
        self,
        request: btrip_open_20220520_models.CommonApplySyncRequest,
    ) -> btrip_open_20220520_models.CommonApplySyncResponse:
        """
        @summary 退改审批结果同步
        
        @param request: CommonApplySyncRequest
        @return: CommonApplySyncResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.CommonApplySyncHeaders()
        return await self.common_apply_sync_with_options_async(request, headers, runtime)

    def cooperator_flight_bill_settlement_query_with_options(
        self,
        request: btrip_open_20220520_models.CooperatorFlightBillSettlementQueryRequest,
        headers: btrip_open_20220520_models.CooperatorFlightBillSettlementQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.CooperatorFlightBillSettlementQueryResponse:
        """
        @summary 查询服务商机票记账数据
        
        @param request: CooperatorFlightBillSettlementQueryRequest
        @param headers: CooperatorFlightBillSettlementQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: CooperatorFlightBillSettlementQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cooperator_id):
            query['cooperator_id'] = request.cooperator_id
        if not UtilClient.is_unset(request.page_no):
            query['page_no'] = request.page_no
        if not UtilClient.is_unset(request.page_size):
            query['page_size'] = request.page_size
        if not UtilClient.is_unset(request.period_end):
            query['period_end'] = request.period_end
        if not UtilClient.is_unset(request.period_start):
            query['period_start'] = request.period_start
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CooperatorFlightBillSettlementQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/cooperator-flight/v1/bill-settlement',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.CooperatorFlightBillSettlementQueryResponse(),
            self.call_api(params, req, runtime)
        )

    async def cooperator_flight_bill_settlement_query_with_options_async(
        self,
        request: btrip_open_20220520_models.CooperatorFlightBillSettlementQueryRequest,
        headers: btrip_open_20220520_models.CooperatorFlightBillSettlementQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.CooperatorFlightBillSettlementQueryResponse:
        """
        @summary 查询服务商机票记账数据
        
        @param request: CooperatorFlightBillSettlementQueryRequest
        @param headers: CooperatorFlightBillSettlementQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: CooperatorFlightBillSettlementQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cooperator_id):
            query['cooperator_id'] = request.cooperator_id
        if not UtilClient.is_unset(request.page_no):
            query['page_no'] = request.page_no
        if not UtilClient.is_unset(request.page_size):
            query['page_size'] = request.page_size
        if not UtilClient.is_unset(request.period_end):
            query['period_end'] = request.period_end
        if not UtilClient.is_unset(request.period_start):
            query['period_start'] = request.period_start
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CooperatorFlightBillSettlementQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/cooperator-flight/v1/bill-settlement',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.CooperatorFlightBillSettlementQueryResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def cooperator_flight_bill_settlement_query(
        self,
        request: btrip_open_20220520_models.CooperatorFlightBillSettlementQueryRequest,
    ) -> btrip_open_20220520_models.CooperatorFlightBillSettlementQueryResponse:
        """
        @summary 查询服务商机票记账数据
        
        @param request: CooperatorFlightBillSettlementQueryRequest
        @return: CooperatorFlightBillSettlementQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.CooperatorFlightBillSettlementQueryHeaders()
        return self.cooperator_flight_bill_settlement_query_with_options(request, headers, runtime)

    async def cooperator_flight_bill_settlement_query_async(
        self,
        request: btrip_open_20220520_models.CooperatorFlightBillSettlementQueryRequest,
    ) -> btrip_open_20220520_models.CooperatorFlightBillSettlementQueryResponse:
        """
        @summary 查询服务商机票记账数据
        
        @param request: CooperatorFlightBillSettlementQueryRequest
        @return: CooperatorFlightBillSettlementQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.CooperatorFlightBillSettlementQueryHeaders()
        return await self.cooperator_flight_bill_settlement_query_with_options_async(request, headers, runtime)

    def cooperator_hotel_bill_settlement_query_with_options(
        self,
        request: btrip_open_20220520_models.CooperatorHotelBillSettlementQueryRequest,
        headers: btrip_open_20220520_models.CooperatorHotelBillSettlementQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.CooperatorHotelBillSettlementQueryResponse:
        """
        @summary 查询服务商酒店记账数据
        
        @param request: CooperatorHotelBillSettlementQueryRequest
        @param headers: CooperatorHotelBillSettlementQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: CooperatorHotelBillSettlementQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cooperator_id):
            query['cooperator_id'] = request.cooperator_id
        if not UtilClient.is_unset(request.page_no):
            query['page_no'] = request.page_no
        if not UtilClient.is_unset(request.page_size):
            query['page_size'] = request.page_size
        if not UtilClient.is_unset(request.period_end):
            query['period_end'] = request.period_end
        if not UtilClient.is_unset(request.period_start):
            query['period_start'] = request.period_start
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CooperatorHotelBillSettlementQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/cooperator-hotel/v1/bill-settlement',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.CooperatorHotelBillSettlementQueryResponse(),
            self.call_api(params, req, runtime)
        )

    async def cooperator_hotel_bill_settlement_query_with_options_async(
        self,
        request: btrip_open_20220520_models.CooperatorHotelBillSettlementQueryRequest,
        headers: btrip_open_20220520_models.CooperatorHotelBillSettlementQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.CooperatorHotelBillSettlementQueryResponse:
        """
        @summary 查询服务商酒店记账数据
        
        @param request: CooperatorHotelBillSettlementQueryRequest
        @param headers: CooperatorHotelBillSettlementQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: CooperatorHotelBillSettlementQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.cooperator_id):
            query['cooperator_id'] = request.cooperator_id
        if not UtilClient.is_unset(request.page_no):
            query['page_no'] = request.page_no
        if not UtilClient.is_unset(request.page_size):
            query['page_size'] = request.page_size
        if not UtilClient.is_unset(request.period_end):
            query['period_end'] = request.period_end
        if not UtilClient.is_unset(request.period_start):
            query['period_start'] = request.period_start
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CooperatorHotelBillSettlementQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/cooperator-hotel/v1/bill-settlement',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.CooperatorHotelBillSettlementQueryResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def cooperator_hotel_bill_settlement_query(
        self,
        request: btrip_open_20220520_models.CooperatorHotelBillSettlementQueryRequest,
    ) -> btrip_open_20220520_models.CooperatorHotelBillSettlementQueryResponse:
        """
        @summary 查询服务商酒店记账数据
        
        @param request: CooperatorHotelBillSettlementQueryRequest
        @return: CooperatorHotelBillSettlementQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.CooperatorHotelBillSettlementQueryHeaders()
        return self.cooperator_hotel_bill_settlement_query_with_options(request, headers, runtime)

    async def cooperator_hotel_bill_settlement_query_async(
        self,
        request: btrip_open_20220520_models.CooperatorHotelBillSettlementQueryRequest,
    ) -> btrip_open_20220520_models.CooperatorHotelBillSettlementQueryResponse:
        """
        @summary 查询服务商酒店记账数据
        
        @param request: CooperatorHotelBillSettlementQueryRequest
        @return: CooperatorHotelBillSettlementQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.CooperatorHotelBillSettlementQueryHeaders()
        return await self.cooperator_hotel_bill_settlement_query_with_options_async(request, headers, runtime)

    def corp_auth_link_info_query_with_options(
        self,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.CorpAuthLinkInfoQueryResponse:
        """
        @summary 获取关联可调用企业接口
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: CorpAuthLinkInfoQueryResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='CorpAuthLinkInfoQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/corp-authority-link/v1/info',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.CorpAuthLinkInfoQueryResponse(),
            self.call_api(params, req, runtime)
        )

    async def corp_auth_link_info_query_with_options_async(
        self,
        headers: Dict[str, str],
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.CorpAuthLinkInfoQueryResponse:
        """
        @summary 获取关联可调用企业接口
        
        @param headers: map
        @param runtime: runtime options for this request RuntimeOptions
        @return: CorpAuthLinkInfoQueryResponse
        """
        req = open_api_models.OpenApiRequest(
            headers=headers
        )
        params = open_api_models.Params(
            action='CorpAuthLinkInfoQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/corp-authority-link/v1/info',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.CorpAuthLinkInfoQueryResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def corp_auth_link_info_query(self) -> btrip_open_20220520_models.CorpAuthLinkInfoQueryResponse:
        """
        @summary 获取关联可调用企业接口
        
        @return: CorpAuthLinkInfoQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return self.corp_auth_link_info_query_with_options(headers, runtime)

    async def corp_auth_link_info_query_async(self) -> btrip_open_20220520_models.CorpAuthLinkInfoQueryResponse:
        """
        @summary 获取关联可调用企业接口
        
        @return: CorpAuthLinkInfoQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = {}
        return await self.corp_auth_link_info_query_with_options_async(headers, runtime)

    def corp_token_with_options(
        self,
        request: btrip_open_20220520_models.CorpTokenRequest,
        headers: btrip_open_20220520_models.CorpTokenHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.CorpTokenResponse:
        """
        @summary 换取CorpToken接口
        
        @param request: CorpTokenRequest
        @param headers: CorpTokenHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: CorpTokenResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.app_secret):
            query['app_secret'] = request.app_secret
        if not UtilClient.is_unset(request.corp_id):
            query['corp_id'] = request.corp_id
        if not UtilClient.is_unset(request.type):
            query['type'] = request.type
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_access_token):
            real_headers['x-acs-btrip-access-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CorpToken',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/btrip-open-auth/v1/corp-token/action/take',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.CorpTokenResponse(),
            self.call_api(params, req, runtime)
        )

    async def corp_token_with_options_async(
        self,
        request: btrip_open_20220520_models.CorpTokenRequest,
        headers: btrip_open_20220520_models.CorpTokenHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.CorpTokenResponse:
        """
        @summary 换取CorpToken接口
        
        @param request: CorpTokenRequest
        @param headers: CorpTokenHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: CorpTokenResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.app_secret):
            query['app_secret'] = request.app_secret
        if not UtilClient.is_unset(request.corp_id):
            query['corp_id'] = request.corp_id
        if not UtilClient.is_unset(request.type):
            query['type'] = request.type
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_access_token):
            real_headers['x-acs-btrip-access-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CorpToken',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/btrip-open-auth/v1/corp-token/action/take',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.CorpTokenResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def corp_token(
        self,
        request: btrip_open_20220520_models.CorpTokenRequest,
    ) -> btrip_open_20220520_models.CorpTokenResponse:
        """
        @summary 换取CorpToken接口
        
        @param request: CorpTokenRequest
        @return: CorpTokenResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.CorpTokenHeaders()
        return self.corp_token_with_options(request, headers, runtime)

    async def corp_token_async(
        self,
        request: btrip_open_20220520_models.CorpTokenRequest,
    ) -> btrip_open_20220520_models.CorpTokenResponse:
        """
        @summary 换取CorpToken接口
        
        @param request: CorpTokenRequest
        @return: CorpTokenResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.CorpTokenHeaders()
        return await self.corp_token_with_options_async(request, headers, runtime)

    def cost_center_delete_with_options(
        self,
        request: btrip_open_20220520_models.CostCenterDeleteRequest,
        headers: btrip_open_20220520_models.CostCenterDeleteHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.CostCenterDeleteResponse:
        """
        @summary 删除成本中心
        
        @param request: CostCenterDeleteRequest
        @param headers: CostCenterDeleteHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: CostCenterDeleteResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.thirdpart_id):
            query['thirdpart_id'] = request.thirdpart_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CostCenterDelete',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/costcenter/v1/delete-costcenter',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.CostCenterDeleteResponse(),
            self.call_api(params, req, runtime)
        )

    async def cost_center_delete_with_options_async(
        self,
        request: btrip_open_20220520_models.CostCenterDeleteRequest,
        headers: btrip_open_20220520_models.CostCenterDeleteHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.CostCenterDeleteResponse:
        """
        @summary 删除成本中心
        
        @param request: CostCenterDeleteRequest
        @param headers: CostCenterDeleteHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: CostCenterDeleteResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.thirdpart_id):
            query['thirdpart_id'] = request.thirdpart_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CostCenterDelete',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/costcenter/v1/delete-costcenter',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.CostCenterDeleteResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def cost_center_delete(
        self,
        request: btrip_open_20220520_models.CostCenterDeleteRequest,
    ) -> btrip_open_20220520_models.CostCenterDeleteResponse:
        """
        @summary 删除成本中心
        
        @param request: CostCenterDeleteRequest
        @return: CostCenterDeleteResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.CostCenterDeleteHeaders()
        return self.cost_center_delete_with_options(request, headers, runtime)

    async def cost_center_delete_async(
        self,
        request: btrip_open_20220520_models.CostCenterDeleteRequest,
    ) -> btrip_open_20220520_models.CostCenterDeleteResponse:
        """
        @summary 删除成本中心
        
        @param request: CostCenterDeleteRequest
        @return: CostCenterDeleteResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.CostCenterDeleteHeaders()
        return await self.cost_center_delete_with_options_async(request, headers, runtime)

    def cost_center_modify_with_options(
        self,
        request: btrip_open_20220520_models.CostCenterModifyRequest,
        headers: btrip_open_20220520_models.CostCenterModifyHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.CostCenterModifyResponse:
        """
        @summary 修改成本中心
        
        @param request: CostCenterModifyRequest
        @param headers: CostCenterModifyHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: CostCenterModifyResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.alipay_no):
            body['alipay_no'] = request.alipay_no
        if not UtilClient.is_unset(request.disable):
            body['disable'] = request.disable
        if not UtilClient.is_unset(request.number):
            body['number'] = request.number
        if not UtilClient.is_unset(request.scope):
            body['scope'] = request.scope
        if not UtilClient.is_unset(request.thirdpart_id):
            body['thirdpart_id'] = request.thirdpart_id
        if not UtilClient.is_unset(request.title):
            body['title'] = request.title
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CostCenterModify',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/costcenter/v1/modify-costcenter',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.CostCenterModifyResponse(),
            self.call_api(params, req, runtime)
        )

    async def cost_center_modify_with_options_async(
        self,
        request: btrip_open_20220520_models.CostCenterModifyRequest,
        headers: btrip_open_20220520_models.CostCenterModifyHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.CostCenterModifyResponse:
        """
        @summary 修改成本中心
        
        @param request: CostCenterModifyRequest
        @param headers: CostCenterModifyHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: CostCenterModifyResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.alipay_no):
            body['alipay_no'] = request.alipay_no
        if not UtilClient.is_unset(request.disable):
            body['disable'] = request.disable
        if not UtilClient.is_unset(request.number):
            body['number'] = request.number
        if not UtilClient.is_unset(request.scope):
            body['scope'] = request.scope
        if not UtilClient.is_unset(request.thirdpart_id):
            body['thirdpart_id'] = request.thirdpart_id
        if not UtilClient.is_unset(request.title):
            body['title'] = request.title
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CostCenterModify',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/costcenter/v1/modify-costcenter',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.CostCenterModifyResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def cost_center_modify(
        self,
        request: btrip_open_20220520_models.CostCenterModifyRequest,
    ) -> btrip_open_20220520_models.CostCenterModifyResponse:
        """
        @summary 修改成本中心
        
        @param request: CostCenterModifyRequest
        @return: CostCenterModifyResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.CostCenterModifyHeaders()
        return self.cost_center_modify_with_options(request, headers, runtime)

    async def cost_center_modify_async(
        self,
        request: btrip_open_20220520_models.CostCenterModifyRequest,
    ) -> btrip_open_20220520_models.CostCenterModifyResponse:
        """
        @summary 修改成本中心
        
        @param request: CostCenterModifyRequest
        @return: CostCenterModifyResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.CostCenterModifyHeaders()
        return await self.cost_center_modify_with_options_async(request, headers, runtime)

    def cost_center_query_with_options(
        self,
        request: btrip_open_20220520_models.CostCenterQueryRequest,
        headers: btrip_open_20220520_models.CostCenterQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.CostCenterQueryResponse:
        """
        @summary 查看成本中心
        
        @param request: CostCenterQueryRequest
        @param headers: CostCenterQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: CostCenterQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.disable):
            query['disable'] = request.disable
        if not UtilClient.is_unset(request.need_org_entity):
            query['need_org_entity'] = request.need_org_entity
        if not UtilClient.is_unset(request.thirdpart_id):
            query['thirdpart_id'] = request.thirdpart_id
        if not UtilClient.is_unset(request.title):
            query['title'] = request.title
        if not UtilClient.is_unset(request.user_id):
            query['user_id'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CostCenterQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/costcenter/v1/costcenter',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.CostCenterQueryResponse(),
            self.call_api(params, req, runtime)
        )

    async def cost_center_query_with_options_async(
        self,
        request: btrip_open_20220520_models.CostCenterQueryRequest,
        headers: btrip_open_20220520_models.CostCenterQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.CostCenterQueryResponse:
        """
        @summary 查看成本中心
        
        @param request: CostCenterQueryRequest
        @param headers: CostCenterQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: CostCenterQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.disable):
            query['disable'] = request.disable
        if not UtilClient.is_unset(request.need_org_entity):
            query['need_org_entity'] = request.need_org_entity
        if not UtilClient.is_unset(request.thirdpart_id):
            query['thirdpart_id'] = request.thirdpart_id
        if not UtilClient.is_unset(request.title):
            query['title'] = request.title
        if not UtilClient.is_unset(request.user_id):
            query['user_id'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='CostCenterQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/costcenter/v1/costcenter',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.CostCenterQueryResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def cost_center_query(
        self,
        request: btrip_open_20220520_models.CostCenterQueryRequest,
    ) -> btrip_open_20220520_models.CostCenterQueryResponse:
        """
        @summary 查看成本中心
        
        @param request: CostCenterQueryRequest
        @return: CostCenterQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.CostCenterQueryHeaders()
        return self.cost_center_query_with_options(request, headers, runtime)

    async def cost_center_query_async(
        self,
        request: btrip_open_20220520_models.CostCenterQueryRequest,
    ) -> btrip_open_20220520_models.CostCenterQueryResponse:
        """
        @summary 查看成本中心
        
        @param request: CostCenterQueryRequest
        @return: CostCenterQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.CostCenterQueryHeaders()
        return await self.cost_center_query_with_options_async(request, headers, runtime)

    def cost_center_save_with_options(
        self,
        request: btrip_open_20220520_models.CostCenterSaveRequest,
        headers: btrip_open_20220520_models.CostCenterSaveHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.CostCenterSaveResponse:
        """
        @summary 保存成本中心
        
        @param request: CostCenterSaveRequest
        @param headers: CostCenterSaveHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: CostCenterSaveResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.alipay_no):
            body['alipay_no'] = request.alipay_no
        if not UtilClient.is_unset(request.disable):
            body['disable'] = request.disable
        if not UtilClient.is_unset(request.number):
            body['number'] = request.number
        if not UtilClient.is_unset(request.scope):
            body['scope'] = request.scope
        if not UtilClient.is_unset(request.thirdpart_id):
            body['thirdpart_id'] = request.thirdpart_id
        if not UtilClient.is_unset(request.title):
            body['title'] = request.title
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CostCenterSave',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/costcenter/v1/save-costcenter',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.CostCenterSaveResponse(),
            self.call_api(params, req, runtime)
        )

    async def cost_center_save_with_options_async(
        self,
        request: btrip_open_20220520_models.CostCenterSaveRequest,
        headers: btrip_open_20220520_models.CostCenterSaveHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.CostCenterSaveResponse:
        """
        @summary 保存成本中心
        
        @param request: CostCenterSaveRequest
        @param headers: CostCenterSaveHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: CostCenterSaveResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.alipay_no):
            body['alipay_no'] = request.alipay_no
        if not UtilClient.is_unset(request.disable):
            body['disable'] = request.disable
        if not UtilClient.is_unset(request.number):
            body['number'] = request.number
        if not UtilClient.is_unset(request.scope):
            body['scope'] = request.scope
        if not UtilClient.is_unset(request.thirdpart_id):
            body['thirdpart_id'] = request.thirdpart_id
        if not UtilClient.is_unset(request.title):
            body['title'] = request.title
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CostCenterSave',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/costcenter/v1/save-costcenter',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.CostCenterSaveResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def cost_center_save(
        self,
        request: btrip_open_20220520_models.CostCenterSaveRequest,
    ) -> btrip_open_20220520_models.CostCenterSaveResponse:
        """
        @summary 保存成本中心
        
        @param request: CostCenterSaveRequest
        @return: CostCenterSaveResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.CostCenterSaveHeaders()
        return self.cost_center_save_with_options(request, headers, runtime)

    async def cost_center_save_async(
        self,
        request: btrip_open_20220520_models.CostCenterSaveRequest,
    ) -> btrip_open_20220520_models.CostCenterSaveResponse:
        """
        @summary 保存成本中心
        
        @param request: CostCenterSaveRequest
        @return: CostCenterSaveResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.CostCenterSaveHeaders()
        return await self.cost_center_save_with_options_async(request, headers, runtime)

    def create_sub_corp_with_options(
        self,
        request: btrip_open_20220520_models.CreateSubCorpRequest,
        headers: btrip_open_20220520_models.CreateSubCorpHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.CreateSubCorpResponse:
        """
        @summary 创建子企业
        
        @param request: CreateSubCorpRequest
        @param headers: CreateSubCorpHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateSubCorpResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.outer_corp_id):
            body['outer_corp_id'] = request.outer_corp_id
        if not UtilClient.is_unset(request.outer_corp_name):
            body['outer_corp_name'] = request.outer_corp_name
        if not UtilClient.is_unset(request.user_id):
            body['user_id'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateSubCorp',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/sub_corps/v1/corps',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.CreateSubCorpResponse(),
            self.call_api(params, req, runtime)
        )

    async def create_sub_corp_with_options_async(
        self,
        request: btrip_open_20220520_models.CreateSubCorpRequest,
        headers: btrip_open_20220520_models.CreateSubCorpHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.CreateSubCorpResponse:
        """
        @summary 创建子企业
        
        @param request: CreateSubCorpRequest
        @param headers: CreateSubCorpHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: CreateSubCorpResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.outer_corp_id):
            body['outer_corp_id'] = request.outer_corp_id
        if not UtilClient.is_unset(request.outer_corp_name):
            body['outer_corp_name'] = request.outer_corp_name
        if not UtilClient.is_unset(request.user_id):
            body['user_id'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='CreateSubCorp',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/sub_corps/v1/corps',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.CreateSubCorpResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def create_sub_corp(
        self,
        request: btrip_open_20220520_models.CreateSubCorpRequest,
    ) -> btrip_open_20220520_models.CreateSubCorpResponse:
        """
        @summary 创建子企业
        
        @param request: CreateSubCorpRequest
        @return: CreateSubCorpResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.CreateSubCorpHeaders()
        return self.create_sub_corp_with_options(request, headers, runtime)

    async def create_sub_corp_async(
        self,
        request: btrip_open_20220520_models.CreateSubCorpRequest,
    ) -> btrip_open_20220520_models.CreateSubCorpResponse:
        """
        @summary 创建子企业
        
        @param request: CreateSubCorpRequest
        @return: CreateSubCorpResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.CreateSubCorpHeaders()
        return await self.create_sub_corp_with_options_async(request, headers, runtime)

    def delete_invoice_entity_with_options(
        self,
        tmp_req: btrip_open_20220520_models.DeleteInvoiceEntityRequest,
        headers: btrip_open_20220520_models.DeleteInvoiceEntityHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.DeleteInvoiceEntityResponse:
        """
        @summary 删除发票抬头适用人员
        
        @param tmp_req: DeleteInvoiceEntityRequest
        @param headers: DeleteInvoiceEntityHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteInvoiceEntityResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.DeleteInvoiceEntityShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.entities):
            request.entities_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.entities, 'entities', 'json')
        query = {}
        if not UtilClient.is_unset(request.del_all):
            query['del_all'] = request.del_all
        if not UtilClient.is_unset(request.entities_shrink):
            query['entities'] = request.entities_shrink
        if not UtilClient.is_unset(request.third_part_id):
            query['third_part_id'] = request.third_part_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteInvoiceEntity',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/invoice/v1/entities',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.DeleteInvoiceEntityResponse(),
            self.call_api(params, req, runtime)
        )

    async def delete_invoice_entity_with_options_async(
        self,
        tmp_req: btrip_open_20220520_models.DeleteInvoiceEntityRequest,
        headers: btrip_open_20220520_models.DeleteInvoiceEntityHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.DeleteInvoiceEntityResponse:
        """
        @summary 删除发票抬头适用人员
        
        @param tmp_req: DeleteInvoiceEntityRequest
        @param headers: DeleteInvoiceEntityHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: DeleteInvoiceEntityResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.DeleteInvoiceEntityShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.entities):
            request.entities_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.entities, 'entities', 'json')
        query = {}
        if not UtilClient.is_unset(request.del_all):
            query['del_all'] = request.del_all
        if not UtilClient.is_unset(request.entities_shrink):
            query['entities'] = request.entities_shrink
        if not UtilClient.is_unset(request.third_part_id):
            query['third_part_id'] = request.third_part_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='DeleteInvoiceEntity',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/invoice/v1/entities',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.DeleteInvoiceEntityResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def delete_invoice_entity(
        self,
        request: btrip_open_20220520_models.DeleteInvoiceEntityRequest,
    ) -> btrip_open_20220520_models.DeleteInvoiceEntityResponse:
        """
        @summary 删除发票抬头适用人员
        
        @param request: DeleteInvoiceEntityRequest
        @return: DeleteInvoiceEntityResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.DeleteInvoiceEntityHeaders()
        return self.delete_invoice_entity_with_options(request, headers, runtime)

    async def delete_invoice_entity_async(
        self,
        request: btrip_open_20220520_models.DeleteInvoiceEntityRequest,
    ) -> btrip_open_20220520_models.DeleteInvoiceEntityResponse:
        """
        @summary 删除发票抬头适用人员
        
        @param request: DeleteInvoiceEntityRequest
        @return: DeleteInvoiceEntityResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.DeleteInvoiceEntityHeaders()
        return await self.delete_invoice_entity_with_options_async(request, headers, runtime)

    def department_save_with_options(
        self,
        tmp_req: btrip_open_20220520_models.DepartmentSaveRequest,
        headers: btrip_open_20220520_models.DepartmentSaveHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.DepartmentSaveResponse:
        """
        @summary 同步外部平台部门信息至商旅内部
        
        @param tmp_req: DepartmentSaveRequest
        @param headers: DepartmentSaveHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: DepartmentSaveResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.DepartmentSaveShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.depart_list):
            request.depart_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.depart_list, 'depart_list', 'json')
        body = {}
        if not UtilClient.is_unset(request.depart_list_shrink):
            body['depart_list'] = request.depart_list_shrink
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='DepartmentSave',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/department/v1/department',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.DepartmentSaveResponse(),
            self.call_api(params, req, runtime)
        )

    async def department_save_with_options_async(
        self,
        tmp_req: btrip_open_20220520_models.DepartmentSaveRequest,
        headers: btrip_open_20220520_models.DepartmentSaveHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.DepartmentSaveResponse:
        """
        @summary 同步外部平台部门信息至商旅内部
        
        @param tmp_req: DepartmentSaveRequest
        @param headers: DepartmentSaveHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: DepartmentSaveResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.DepartmentSaveShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.depart_list):
            request.depart_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.depart_list, 'depart_list', 'json')
        body = {}
        if not UtilClient.is_unset(request.depart_list_shrink):
            body['depart_list'] = request.depart_list_shrink
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='DepartmentSave',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/department/v1/department',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.DepartmentSaveResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def department_save(
        self,
        request: btrip_open_20220520_models.DepartmentSaveRequest,
    ) -> btrip_open_20220520_models.DepartmentSaveResponse:
        """
        @summary 同步外部平台部门信息至商旅内部
        
        @param request: DepartmentSaveRequest
        @return: DepartmentSaveResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.DepartmentSaveHeaders()
        return self.department_save_with_options(request, headers, runtime)

    async def department_save_async(
        self,
        request: btrip_open_20220520_models.DepartmentSaveRequest,
    ) -> btrip_open_20220520_models.DepartmentSaveResponse:
        """
        @summary 同步外部平台部门信息至商旅内部
        
        @param request: DepartmentSaveRequest
        @return: DepartmentSaveResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.DepartmentSaveHeaders()
        return await self.department_save_with_options_async(request, headers, runtime)

    def entity_add_with_options(
        self,
        tmp_req: btrip_open_20220520_models.EntityAddRequest,
        headers: btrip_open_20220520_models.EntityAddHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.EntityAddResponse:
        """
        @summary 增加成本中心人员信息
        
        @param tmp_req: EntityAddRequest
        @param headers: EntityAddHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: EntityAddResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.EntityAddShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.entity_dolist):
            request.entity_dolist_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.entity_dolist, 'entity_d_o_list', 'json')
        body = {}
        if not UtilClient.is_unset(request.entity_dolist_shrink):
            body['entity_d_o_list'] = request.entity_dolist_shrink
        if not UtilClient.is_unset(request.thirdpart_id):
            body['thirdpart_id'] = request.thirdpart_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='EntityAdd',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/costcenter/v1/add-entity',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.EntityAddResponse(),
            self.call_api(params, req, runtime)
        )

    async def entity_add_with_options_async(
        self,
        tmp_req: btrip_open_20220520_models.EntityAddRequest,
        headers: btrip_open_20220520_models.EntityAddHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.EntityAddResponse:
        """
        @summary 增加成本中心人员信息
        
        @param tmp_req: EntityAddRequest
        @param headers: EntityAddHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: EntityAddResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.EntityAddShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.entity_dolist):
            request.entity_dolist_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.entity_dolist, 'entity_d_o_list', 'json')
        body = {}
        if not UtilClient.is_unset(request.entity_dolist_shrink):
            body['entity_d_o_list'] = request.entity_dolist_shrink
        if not UtilClient.is_unset(request.thirdpart_id):
            body['thirdpart_id'] = request.thirdpart_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='EntityAdd',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/costcenter/v1/add-entity',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.EntityAddResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def entity_add(
        self,
        request: btrip_open_20220520_models.EntityAddRequest,
    ) -> btrip_open_20220520_models.EntityAddResponse:
        """
        @summary 增加成本中心人员信息
        
        @param request: EntityAddRequest
        @return: EntityAddResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.EntityAddHeaders()
        return self.entity_add_with_options(request, headers, runtime)

    async def entity_add_async(
        self,
        request: btrip_open_20220520_models.EntityAddRequest,
    ) -> btrip_open_20220520_models.EntityAddResponse:
        """
        @summary 增加成本中心人员信息
        
        @param request: EntityAddRequest
        @return: EntityAddResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.EntityAddHeaders()
        return await self.entity_add_with_options_async(request, headers, runtime)

    def entity_delete_with_options(
        self,
        tmp_req: btrip_open_20220520_models.EntityDeleteRequest,
        headers: btrip_open_20220520_models.EntityDeleteHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.EntityDeleteResponse:
        """
        @summary 删除成本中心人员信息
        
        @param tmp_req: EntityDeleteRequest
        @param headers: EntityDeleteHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: EntityDeleteResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.EntityDeleteShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.entity_dolist):
            request.entity_dolist_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.entity_dolist, 'entity_d_o_list', 'json')
        query = {}
        if not UtilClient.is_unset(request.del_all):
            query['del_all'] = request.del_all
        if not UtilClient.is_unset(request.thirdpart_id):
            query['thirdpart_id'] = request.thirdpart_id
        body = {}
        if not UtilClient.is_unset(request.entity_dolist_shrink):
            body['entity_d_o_list'] = request.entity_dolist_shrink
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='EntityDelete',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/costcenter/v1/entity/action/delete',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.EntityDeleteResponse(),
            self.call_api(params, req, runtime)
        )

    async def entity_delete_with_options_async(
        self,
        tmp_req: btrip_open_20220520_models.EntityDeleteRequest,
        headers: btrip_open_20220520_models.EntityDeleteHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.EntityDeleteResponse:
        """
        @summary 删除成本中心人员信息
        
        @param tmp_req: EntityDeleteRequest
        @param headers: EntityDeleteHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: EntityDeleteResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.EntityDeleteShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.entity_dolist):
            request.entity_dolist_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.entity_dolist, 'entity_d_o_list', 'json')
        query = {}
        if not UtilClient.is_unset(request.del_all):
            query['del_all'] = request.del_all
        if not UtilClient.is_unset(request.thirdpart_id):
            query['thirdpart_id'] = request.thirdpart_id
        body = {}
        if not UtilClient.is_unset(request.entity_dolist_shrink):
            body['entity_d_o_list'] = request.entity_dolist_shrink
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='EntityDelete',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/costcenter/v1/entity/action/delete',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.EntityDeleteResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def entity_delete(
        self,
        request: btrip_open_20220520_models.EntityDeleteRequest,
    ) -> btrip_open_20220520_models.EntityDeleteResponse:
        """
        @summary 删除成本中心人员信息
        
        @param request: EntityDeleteRequest
        @return: EntityDeleteResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.EntityDeleteHeaders()
        return self.entity_delete_with_options(request, headers, runtime)

    async def entity_delete_async(
        self,
        request: btrip_open_20220520_models.EntityDeleteRequest,
    ) -> btrip_open_20220520_models.EntityDeleteResponse:
        """
        @summary 删除成本中心人员信息
        
        @param request: EntityDeleteRequest
        @return: EntityDeleteResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.EntityDeleteHeaders()
        return await self.entity_delete_with_options_async(request, headers, runtime)

    def entity_set_with_options(
        self,
        tmp_req: btrip_open_20220520_models.EntitySetRequest,
        headers: btrip_open_20220520_models.EntitySetHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.EntitySetResponse:
        """
        @summary 设置成本中心人员信息
        
        @param tmp_req: EntitySetRequest
        @param headers: EntitySetHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: EntitySetResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.EntitySetShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.entity_dolist):
            request.entity_dolist_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.entity_dolist, 'entity_d_o_list', 'json')
        body = {}
        if not UtilClient.is_unset(request.entity_dolist_shrink):
            body['entity_d_o_list'] = request.entity_dolist_shrink
        if not UtilClient.is_unset(request.thirdpart_id):
            body['thirdpart_id'] = request.thirdpart_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='EntitySet',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/costcenter/v1/set-entity',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.EntitySetResponse(),
            self.call_api(params, req, runtime)
        )

    async def entity_set_with_options_async(
        self,
        tmp_req: btrip_open_20220520_models.EntitySetRequest,
        headers: btrip_open_20220520_models.EntitySetHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.EntitySetResponse:
        """
        @summary 设置成本中心人员信息
        
        @param tmp_req: EntitySetRequest
        @param headers: EntitySetHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: EntitySetResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.EntitySetShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.entity_dolist):
            request.entity_dolist_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.entity_dolist, 'entity_d_o_list', 'json')
        body = {}
        if not UtilClient.is_unset(request.entity_dolist_shrink):
            body['entity_d_o_list'] = request.entity_dolist_shrink
        if not UtilClient.is_unset(request.thirdpart_id):
            body['thirdpart_id'] = request.thirdpart_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='EntitySet',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/costcenter/v1/set-entity',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.EntitySetResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def entity_set(
        self,
        request: btrip_open_20220520_models.EntitySetRequest,
    ) -> btrip_open_20220520_models.EntitySetResponse:
        """
        @summary 设置成本中心人员信息
        
        @param request: EntitySetRequest
        @return: EntitySetResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.EntitySetHeaders()
        return self.entity_set_with_options(request, headers, runtime)

    async def entity_set_async(
        self,
        request: btrip_open_20220520_models.EntitySetRequest,
    ) -> btrip_open_20220520_models.EntitySetResponse:
        """
        @summary 设置成本中心人员信息
        
        @param request: EntitySetRequest
        @return: EntitySetResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.EntitySetHeaders()
        return await self.entity_set_with_options_async(request, headers, runtime)

    def estimated_price_query_with_options(
        self,
        request: btrip_open_20220520_models.EstimatedPriceQueryRequest,
        headers: btrip_open_20220520_models.EstimatedPriceQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.EstimatedPriceQueryResponse:
        """
        @summary 预估价格查询
        
        @param request: EstimatedPriceQueryRequest
        @param headers: EstimatedPriceQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: EstimatedPriceQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.arr_city):
            query['arr_city'] = request.arr_city
        if not UtilClient.is_unset(request.category):
            query['category'] = request.category
        if not UtilClient.is_unset(request.dep_city):
            query['dep_city'] = request.dep_city
        if not UtilClient.is_unset(request.end_time):
            query['end_time'] = request.end_time
        if not UtilClient.is_unset(request.itinerary_id):
            query['itinerary_id'] = request.itinerary_id
        if not UtilClient.is_unset(request.start_time):
            query['start_time'] = request.start_time
        if not UtilClient.is_unset(request.sub_corp_id):
            query['sub_corp_id'] = request.sub_corp_id
        if not UtilClient.is_unset(request.user_id):
            query['user_id'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='EstimatedPriceQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/costcenter/v1/estimated-price',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.EstimatedPriceQueryResponse(),
            self.call_api(params, req, runtime)
        )

    async def estimated_price_query_with_options_async(
        self,
        request: btrip_open_20220520_models.EstimatedPriceQueryRequest,
        headers: btrip_open_20220520_models.EstimatedPriceQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.EstimatedPriceQueryResponse:
        """
        @summary 预估价格查询
        
        @param request: EstimatedPriceQueryRequest
        @param headers: EstimatedPriceQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: EstimatedPriceQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.arr_city):
            query['arr_city'] = request.arr_city
        if not UtilClient.is_unset(request.category):
            query['category'] = request.category
        if not UtilClient.is_unset(request.dep_city):
            query['dep_city'] = request.dep_city
        if not UtilClient.is_unset(request.end_time):
            query['end_time'] = request.end_time
        if not UtilClient.is_unset(request.itinerary_id):
            query['itinerary_id'] = request.itinerary_id
        if not UtilClient.is_unset(request.start_time):
            query['start_time'] = request.start_time
        if not UtilClient.is_unset(request.sub_corp_id):
            query['sub_corp_id'] = request.sub_corp_id
        if not UtilClient.is_unset(request.user_id):
            query['user_id'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='EstimatedPriceQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/costcenter/v1/estimated-price',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.EstimatedPriceQueryResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def estimated_price_query(
        self,
        request: btrip_open_20220520_models.EstimatedPriceQueryRequest,
    ) -> btrip_open_20220520_models.EstimatedPriceQueryResponse:
        """
        @summary 预估价格查询
        
        @param request: EstimatedPriceQueryRequest
        @return: EstimatedPriceQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.EstimatedPriceQueryHeaders()
        return self.estimated_price_query_with_options(request, headers, runtime)

    async def estimated_price_query_async(
        self,
        request: btrip_open_20220520_models.EstimatedPriceQueryRequest,
    ) -> btrip_open_20220520_models.EstimatedPriceQueryResponse:
        """
        @summary 预估价格查询
        
        @param request: EstimatedPriceQueryRequest
        @return: EstimatedPriceQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.EstimatedPriceQueryHeaders()
        return await self.estimated_price_query_with_options_async(request, headers, runtime)

    def exceed_apply_sync_with_options(
        self,
        request: btrip_open_20220520_models.ExceedApplySyncRequest,
        headers: btrip_open_20220520_models.ExceedApplySyncHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.ExceedApplySyncResponse:
        """
        @summary 超标审批结果同步
        
        @param request: ExceedApplySyncRequest
        @param headers: ExceedApplySyncHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: ExceedApplySyncResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.apply_id):
            query['apply_id'] = request.apply_id
        if not UtilClient.is_unset(request.biz_category):
            query['biz_category'] = request.biz_category
        if not UtilClient.is_unset(request.remark):
            query['remark'] = request.remark
        if not UtilClient.is_unset(request.status):
            query['status'] = request.status
        if not UtilClient.is_unset(request.thirdparty_flow_id):
            query['thirdparty_flow_id'] = request.thirdparty_flow_id
        if not UtilClient.is_unset(request.user_id):
            query['user_id'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ExceedApplySync',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/apply/v1/syn-exceed',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.ExceedApplySyncResponse(),
            self.call_api(params, req, runtime)
        )

    async def exceed_apply_sync_with_options_async(
        self,
        request: btrip_open_20220520_models.ExceedApplySyncRequest,
        headers: btrip_open_20220520_models.ExceedApplySyncHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.ExceedApplySyncResponse:
        """
        @summary 超标审批结果同步
        
        @param request: ExceedApplySyncRequest
        @param headers: ExceedApplySyncHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: ExceedApplySyncResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.apply_id):
            query['apply_id'] = request.apply_id
        if not UtilClient.is_unset(request.biz_category):
            query['biz_category'] = request.biz_category
        if not UtilClient.is_unset(request.remark):
            query['remark'] = request.remark
        if not UtilClient.is_unset(request.status):
            query['status'] = request.status
        if not UtilClient.is_unset(request.thirdparty_flow_id):
            query['thirdparty_flow_id'] = request.thirdparty_flow_id
        if not UtilClient.is_unset(request.user_id):
            query['user_id'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ExceedApplySync',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/apply/v1/syn-exceed',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.ExceedApplySyncResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def exceed_apply_sync(
        self,
        request: btrip_open_20220520_models.ExceedApplySyncRequest,
    ) -> btrip_open_20220520_models.ExceedApplySyncResponse:
        """
        @summary 超标审批结果同步
        
        @param request: ExceedApplySyncRequest
        @return: ExceedApplySyncResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.ExceedApplySyncHeaders()
        return self.exceed_apply_sync_with_options(request, headers, runtime)

    async def exceed_apply_sync_async(
        self,
        request: btrip_open_20220520_models.ExceedApplySyncRequest,
    ) -> btrip_open_20220520_models.ExceedApplySyncResponse:
        """
        @summary 超标审批结果同步
        
        @param request: ExceedApplySyncRequest
        @return: ExceedApplySyncResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.ExceedApplySyncHeaders()
        return await self.exceed_apply_sync_with_options_async(request, headers, runtime)

    def flight_bill_settlement_query_with_options(
        self,
        request: btrip_open_20220520_models.FlightBillSettlementQueryRequest,
        headers: btrip_open_20220520_models.FlightBillSettlementQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightBillSettlementQueryResponse:
        """
        @summary 查询机票记账数据
        
        @param request: FlightBillSettlementQueryRequest
        @param headers: FlightBillSettlementQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightBillSettlementQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.page_no):
            query['page_no'] = request.page_no
        if not UtilClient.is_unset(request.page_size):
            query['page_size'] = request.page_size
        if not UtilClient.is_unset(request.period_end):
            query['period_end'] = request.period_end
        if not UtilClient.is_unset(request.period_start):
            query['period_start'] = request.period_start
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='FlightBillSettlementQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/flight/v1/bill-settlement',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightBillSettlementQueryResponse(),
            self.call_api(params, req, runtime)
        )

    async def flight_bill_settlement_query_with_options_async(
        self,
        request: btrip_open_20220520_models.FlightBillSettlementQueryRequest,
        headers: btrip_open_20220520_models.FlightBillSettlementQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightBillSettlementQueryResponse:
        """
        @summary 查询机票记账数据
        
        @param request: FlightBillSettlementQueryRequest
        @param headers: FlightBillSettlementQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightBillSettlementQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.page_no):
            query['page_no'] = request.page_no
        if not UtilClient.is_unset(request.page_size):
            query['page_size'] = request.page_size
        if not UtilClient.is_unset(request.period_end):
            query['period_end'] = request.period_end
        if not UtilClient.is_unset(request.period_start):
            query['period_start'] = request.period_start
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='FlightBillSettlementQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/flight/v1/bill-settlement',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightBillSettlementQueryResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def flight_bill_settlement_query(
        self,
        request: btrip_open_20220520_models.FlightBillSettlementQueryRequest,
    ) -> btrip_open_20220520_models.FlightBillSettlementQueryResponse:
        """
        @summary 查询机票记账数据
        
        @param request: FlightBillSettlementQueryRequest
        @return: FlightBillSettlementQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightBillSettlementQueryHeaders()
        return self.flight_bill_settlement_query_with_options(request, headers, runtime)

    async def flight_bill_settlement_query_async(
        self,
        request: btrip_open_20220520_models.FlightBillSettlementQueryRequest,
    ) -> btrip_open_20220520_models.FlightBillSettlementQueryResponse:
        """
        @summary 查询机票记账数据
        
        @param request: FlightBillSettlementQueryRequest
        @return: FlightBillSettlementQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightBillSettlementQueryHeaders()
        return await self.flight_bill_settlement_query_with_options_async(request, headers, runtime)

    def flight_cancel_order_with_options(
        self,
        request: btrip_open_20220520_models.FlightCancelOrderRequest,
        headers: btrip_open_20220520_models.FlightCancelOrderHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightCancelOrderResponse:
        """
        @summary 航班订单取消
        
        @param request: FlightCancelOrderRequest
        @param headers: FlightCancelOrderHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightCancelOrderResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.dis_order_id):
            query['dis_order_id'] = request.dis_order_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='FlightCancelOrder',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v1/order/action/cancel',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightCancelOrderResponse(),
            self.call_api(params, req, runtime)
        )

    async def flight_cancel_order_with_options_async(
        self,
        request: btrip_open_20220520_models.FlightCancelOrderRequest,
        headers: btrip_open_20220520_models.FlightCancelOrderHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightCancelOrderResponse:
        """
        @summary 航班订单取消
        
        @param request: FlightCancelOrderRequest
        @param headers: FlightCancelOrderHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightCancelOrderResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.dis_order_id):
            query['dis_order_id'] = request.dis_order_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='FlightCancelOrder',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v1/order/action/cancel',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightCancelOrderResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def flight_cancel_order(
        self,
        request: btrip_open_20220520_models.FlightCancelOrderRequest,
    ) -> btrip_open_20220520_models.FlightCancelOrderResponse:
        """
        @summary 航班订单取消
        
        @param request: FlightCancelOrderRequest
        @return: FlightCancelOrderResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightCancelOrderHeaders()
        return self.flight_cancel_order_with_options(request, headers, runtime)

    async def flight_cancel_order_async(
        self,
        request: btrip_open_20220520_models.FlightCancelOrderRequest,
    ) -> btrip_open_20220520_models.FlightCancelOrderResponse:
        """
        @summary 航班订单取消
        
        @param request: FlightCancelOrderRequest
        @return: FlightCancelOrderResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightCancelOrderHeaders()
        return await self.flight_cancel_order_with_options_async(request, headers, runtime)

    def flight_cancel_order_v2with_options(
        self,
        request: btrip_open_20220520_models.FlightCancelOrderV2Request,
        headers: btrip_open_20220520_models.FlightCancelOrderV2Headers,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightCancelOrderV2Response:
        """
        @summary 机票订单取消
        
        @param request: FlightCancelOrderV2Request
        @param headers: FlightCancelOrderV2Headers
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightCancelOrderV2Response
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.isv_name):
            query['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.order_id):
            query['order_id'] = request.order_id
        if not UtilClient.is_unset(request.out_order_id):
            query['out_order_id'] = request.out_order_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='FlightCancelOrderV2',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v2/order/action/cancel',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightCancelOrderV2Response(),
            self.call_api(params, req, runtime)
        )

    async def flight_cancel_order_v2with_options_async(
        self,
        request: btrip_open_20220520_models.FlightCancelOrderV2Request,
        headers: btrip_open_20220520_models.FlightCancelOrderV2Headers,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightCancelOrderV2Response:
        """
        @summary 机票订单取消
        
        @param request: FlightCancelOrderV2Request
        @param headers: FlightCancelOrderV2Headers
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightCancelOrderV2Response
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.isv_name):
            query['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.order_id):
            query['order_id'] = request.order_id
        if not UtilClient.is_unset(request.out_order_id):
            query['out_order_id'] = request.out_order_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='FlightCancelOrderV2',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v2/order/action/cancel',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightCancelOrderV2Response(),
            await self.call_api_async(params, req, runtime)
        )

    def flight_cancel_order_v2(
        self,
        request: btrip_open_20220520_models.FlightCancelOrderV2Request,
    ) -> btrip_open_20220520_models.FlightCancelOrderV2Response:
        """
        @summary 机票订单取消
        
        @param request: FlightCancelOrderV2Request
        @return: FlightCancelOrderV2Response
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightCancelOrderV2Headers()
        return self.flight_cancel_order_v2with_options(request, headers, runtime)

    async def flight_cancel_order_v2_async(
        self,
        request: btrip_open_20220520_models.FlightCancelOrderV2Request,
    ) -> btrip_open_20220520_models.FlightCancelOrderV2Response:
        """
        @summary 机票订单取消
        
        @param request: FlightCancelOrderV2Request
        @return: FlightCancelOrderV2Response
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightCancelOrderV2Headers()
        return await self.flight_cancel_order_v2with_options_async(request, headers, runtime)

    def flight_create_order_with_options(
        self,
        tmp_req: btrip_open_20220520_models.FlightCreateOrderRequest,
        headers: btrip_open_20220520_models.FlightCreateOrderHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightCreateOrderResponse:
        """
        @summary 航班订单创建
        
        @param tmp_req: FlightCreateOrderRequest
        @param headers: FlightCreateOrderHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightCreateOrderResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.FlightCreateOrderShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.contact_info):
            request.contact_info_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.contact_info, 'contact_info', 'json')
        if not UtilClient.is_unset(tmp_req.order_attr):
            request.order_attr_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.order_attr, 'order_attr', 'json')
        if not UtilClient.is_unset(tmp_req.traveler_info_list):
            request.traveler_info_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.traveler_info_list, 'traveler_info_list', 'json')
        body = {}
        if not UtilClient.is_unset(request.arr_airport_code):
            body['arr_airport_code'] = request.arr_airport_code
        if not UtilClient.is_unset(request.arr_city_code):
            body['arr_city_code'] = request.arr_city_code
        if not UtilClient.is_unset(request.auto_pay):
            body['auto_pay'] = request.auto_pay
        if not UtilClient.is_unset(request.buyer_name):
            body['buyer_name'] = request.buyer_name
        if not UtilClient.is_unset(request.buyer_unique_key):
            body['buyer_unique_key'] = request.buyer_unique_key
        if not UtilClient.is_unset(request.contact_info_shrink):
            body['contact_info'] = request.contact_info_shrink
        if not UtilClient.is_unset(request.dep_airport_code):
            body['dep_airport_code'] = request.dep_airport_code
        if not UtilClient.is_unset(request.dep_city_code):
            body['dep_city_code'] = request.dep_city_code
        if not UtilClient.is_unset(request.dep_date):
            body['dep_date'] = request.dep_date
        if not UtilClient.is_unset(request.dis_order_id):
            body['dis_order_id'] = request.dis_order_id
        if not UtilClient.is_unset(request.order_attr_shrink):
            body['order_attr'] = request.order_attr_shrink
        if not UtilClient.is_unset(request.order_params):
            body['order_params'] = request.order_params
        if not UtilClient.is_unset(request.ota_item_id):
            body['ota_item_id'] = request.ota_item_id
        if not UtilClient.is_unset(request.price):
            body['price'] = request.price
        if not UtilClient.is_unset(request.receipt_address):
            body['receipt_address'] = request.receipt_address
        if not UtilClient.is_unset(request.receipt_target):
            body['receipt_target'] = request.receipt_target
        if not UtilClient.is_unset(request.receipt_title):
            body['receipt_title'] = request.receipt_title
        if not UtilClient.is_unset(request.traveler_info_list_shrink):
            body['traveler_info_list'] = request.traveler_info_list_shrink
        if not UtilClient.is_unset(request.trip_type):
            body['trip_type'] = request.trip_type
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='FlightCreateOrder',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v1/order/action/create',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightCreateOrderResponse(),
            self.call_api(params, req, runtime)
        )

    async def flight_create_order_with_options_async(
        self,
        tmp_req: btrip_open_20220520_models.FlightCreateOrderRequest,
        headers: btrip_open_20220520_models.FlightCreateOrderHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightCreateOrderResponse:
        """
        @summary 航班订单创建
        
        @param tmp_req: FlightCreateOrderRequest
        @param headers: FlightCreateOrderHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightCreateOrderResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.FlightCreateOrderShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.contact_info):
            request.contact_info_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.contact_info, 'contact_info', 'json')
        if not UtilClient.is_unset(tmp_req.order_attr):
            request.order_attr_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.order_attr, 'order_attr', 'json')
        if not UtilClient.is_unset(tmp_req.traveler_info_list):
            request.traveler_info_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.traveler_info_list, 'traveler_info_list', 'json')
        body = {}
        if not UtilClient.is_unset(request.arr_airport_code):
            body['arr_airport_code'] = request.arr_airport_code
        if not UtilClient.is_unset(request.arr_city_code):
            body['arr_city_code'] = request.arr_city_code
        if not UtilClient.is_unset(request.auto_pay):
            body['auto_pay'] = request.auto_pay
        if not UtilClient.is_unset(request.buyer_name):
            body['buyer_name'] = request.buyer_name
        if not UtilClient.is_unset(request.buyer_unique_key):
            body['buyer_unique_key'] = request.buyer_unique_key
        if not UtilClient.is_unset(request.contact_info_shrink):
            body['contact_info'] = request.contact_info_shrink
        if not UtilClient.is_unset(request.dep_airport_code):
            body['dep_airport_code'] = request.dep_airport_code
        if not UtilClient.is_unset(request.dep_city_code):
            body['dep_city_code'] = request.dep_city_code
        if not UtilClient.is_unset(request.dep_date):
            body['dep_date'] = request.dep_date
        if not UtilClient.is_unset(request.dis_order_id):
            body['dis_order_id'] = request.dis_order_id
        if not UtilClient.is_unset(request.order_attr_shrink):
            body['order_attr'] = request.order_attr_shrink
        if not UtilClient.is_unset(request.order_params):
            body['order_params'] = request.order_params
        if not UtilClient.is_unset(request.ota_item_id):
            body['ota_item_id'] = request.ota_item_id
        if not UtilClient.is_unset(request.price):
            body['price'] = request.price
        if not UtilClient.is_unset(request.receipt_address):
            body['receipt_address'] = request.receipt_address
        if not UtilClient.is_unset(request.receipt_target):
            body['receipt_target'] = request.receipt_target
        if not UtilClient.is_unset(request.receipt_title):
            body['receipt_title'] = request.receipt_title
        if not UtilClient.is_unset(request.traveler_info_list_shrink):
            body['traveler_info_list'] = request.traveler_info_list_shrink
        if not UtilClient.is_unset(request.trip_type):
            body['trip_type'] = request.trip_type
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='FlightCreateOrder',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v1/order/action/create',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightCreateOrderResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def flight_create_order(
        self,
        request: btrip_open_20220520_models.FlightCreateOrderRequest,
    ) -> btrip_open_20220520_models.FlightCreateOrderResponse:
        """
        @summary 航班订单创建
        
        @param request: FlightCreateOrderRequest
        @return: FlightCreateOrderResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightCreateOrderHeaders()
        return self.flight_create_order_with_options(request, headers, runtime)

    async def flight_create_order_async(
        self,
        request: btrip_open_20220520_models.FlightCreateOrderRequest,
    ) -> btrip_open_20220520_models.FlightCreateOrderResponse:
        """
        @summary 航班订单创建
        
        @param request: FlightCreateOrderRequest
        @return: FlightCreateOrderResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightCreateOrderHeaders()
        return await self.flight_create_order_with_options_async(request, headers, runtime)

    def flight_create_order_v2with_options(
        self,
        tmp_req: btrip_open_20220520_models.FlightCreateOrderV2Request,
        headers: btrip_open_20220520_models.FlightCreateOrderV2Headers,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightCreateOrderV2Response:
        """
        @summary 机票订单创建
        
        @param tmp_req: FlightCreateOrderV2Request
        @param headers: FlightCreateOrderV2Headers
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightCreateOrderV2Response
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.FlightCreateOrderV2ShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.contact_info):
            request.contact_info_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.contact_info, 'contact_info', 'json')
        if not UtilClient.is_unset(tmp_req.travelers):
            request.travelers_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.travelers, 'travelers', 'json')
        body = {}
        if not UtilClient.is_unset(request.async_create_order_key):
            body['async_create_order_key'] = request.async_create_order_key
        if not UtilClient.is_unset(request.async_create_order_mode):
            body['async_create_order_mode'] = request.async_create_order_mode
        if not UtilClient.is_unset(request.btrip_user_id):
            body['btrip_user_id'] = request.btrip_user_id
        if not UtilClient.is_unset(request.buyer_name):
            body['buyer_name'] = request.buyer_name
        if not UtilClient.is_unset(request.contact_info_shrink):
            body['contact_info'] = request.contact_info_shrink
        if not UtilClient.is_unset(request.isv_name):
            body['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.ota_item_id):
            body['ota_item_id'] = request.ota_item_id
        if not UtilClient.is_unset(request.out_order_id):
            body['out_order_id'] = request.out_order_id
        if not UtilClient.is_unset(request.total_price_cent):
            body['total_price_cent'] = request.total_price_cent
        if not UtilClient.is_unset(request.travelers_shrink):
            body['travelers'] = request.travelers_shrink
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='FlightCreateOrderV2',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v2/order/action/create',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightCreateOrderV2Response(),
            self.call_api(params, req, runtime)
        )

    async def flight_create_order_v2with_options_async(
        self,
        tmp_req: btrip_open_20220520_models.FlightCreateOrderV2Request,
        headers: btrip_open_20220520_models.FlightCreateOrderV2Headers,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightCreateOrderV2Response:
        """
        @summary 机票订单创建
        
        @param tmp_req: FlightCreateOrderV2Request
        @param headers: FlightCreateOrderV2Headers
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightCreateOrderV2Response
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.FlightCreateOrderV2ShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.contact_info):
            request.contact_info_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.contact_info, 'contact_info', 'json')
        if not UtilClient.is_unset(tmp_req.travelers):
            request.travelers_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.travelers, 'travelers', 'json')
        body = {}
        if not UtilClient.is_unset(request.async_create_order_key):
            body['async_create_order_key'] = request.async_create_order_key
        if not UtilClient.is_unset(request.async_create_order_mode):
            body['async_create_order_mode'] = request.async_create_order_mode
        if not UtilClient.is_unset(request.btrip_user_id):
            body['btrip_user_id'] = request.btrip_user_id
        if not UtilClient.is_unset(request.buyer_name):
            body['buyer_name'] = request.buyer_name
        if not UtilClient.is_unset(request.contact_info_shrink):
            body['contact_info'] = request.contact_info_shrink
        if not UtilClient.is_unset(request.isv_name):
            body['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.ota_item_id):
            body['ota_item_id'] = request.ota_item_id
        if not UtilClient.is_unset(request.out_order_id):
            body['out_order_id'] = request.out_order_id
        if not UtilClient.is_unset(request.total_price_cent):
            body['total_price_cent'] = request.total_price_cent
        if not UtilClient.is_unset(request.travelers_shrink):
            body['travelers'] = request.travelers_shrink
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='FlightCreateOrderV2',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v2/order/action/create',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightCreateOrderV2Response(),
            await self.call_api_async(params, req, runtime)
        )

    def flight_create_order_v2(
        self,
        request: btrip_open_20220520_models.FlightCreateOrderV2Request,
    ) -> btrip_open_20220520_models.FlightCreateOrderV2Response:
        """
        @summary 机票订单创建
        
        @param request: FlightCreateOrderV2Request
        @return: FlightCreateOrderV2Response
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightCreateOrderV2Headers()
        return self.flight_create_order_v2with_options(request, headers, runtime)

    async def flight_create_order_v2_async(
        self,
        request: btrip_open_20220520_models.FlightCreateOrderV2Request,
    ) -> btrip_open_20220520_models.FlightCreateOrderV2Response:
        """
        @summary 机票订单创建
        
        @param request: FlightCreateOrderV2Request
        @return: FlightCreateOrderV2Response
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightCreateOrderV2Headers()
        return await self.flight_create_order_v2with_options_async(request, headers, runtime)

    def flight_exceed_apply_query_with_options(
        self,
        request: btrip_open_20220520_models.FlightExceedApplyQueryRequest,
        headers: btrip_open_20220520_models.FlightExceedApplyQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightExceedApplyQueryResponse:
        """
        @summary 查询飞机超标审批详情
        
        @param request: FlightExceedApplyQueryRequest
        @param headers: FlightExceedApplyQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightExceedApplyQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.apply_id):
            query['apply_id'] = request.apply_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='FlightExceedApplyQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/apply/v1/flight-exceed',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightExceedApplyQueryResponse(),
            self.call_api(params, req, runtime)
        )

    async def flight_exceed_apply_query_with_options_async(
        self,
        request: btrip_open_20220520_models.FlightExceedApplyQueryRequest,
        headers: btrip_open_20220520_models.FlightExceedApplyQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightExceedApplyQueryResponse:
        """
        @summary 查询飞机超标审批详情
        
        @param request: FlightExceedApplyQueryRequest
        @param headers: FlightExceedApplyQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightExceedApplyQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.apply_id):
            query['apply_id'] = request.apply_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='FlightExceedApplyQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/apply/v1/flight-exceed',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightExceedApplyQueryResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def flight_exceed_apply_query(
        self,
        request: btrip_open_20220520_models.FlightExceedApplyQueryRequest,
    ) -> btrip_open_20220520_models.FlightExceedApplyQueryResponse:
        """
        @summary 查询飞机超标审批详情
        
        @param request: FlightExceedApplyQueryRequest
        @return: FlightExceedApplyQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightExceedApplyQueryHeaders()
        return self.flight_exceed_apply_query_with_options(request, headers, runtime)

    async def flight_exceed_apply_query_async(
        self,
        request: btrip_open_20220520_models.FlightExceedApplyQueryRequest,
    ) -> btrip_open_20220520_models.FlightExceedApplyQueryResponse:
        """
        @summary 查询飞机超标审批详情
        
        @param request: FlightExceedApplyQueryRequest
        @return: FlightExceedApplyQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightExceedApplyQueryHeaders()
        return await self.flight_exceed_apply_query_with_options_async(request, headers, runtime)

    def flight_itinerary_scan_query_with_options(
        self,
        request: btrip_open_20220520_models.FlightItineraryScanQueryRequest,
        headers: btrip_open_20220520_models.FlightItineraryScanQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightItineraryScanQueryResponse:
        """
        @summary 查询机票行程单扫描件
        
        @param request: FlightItineraryScanQueryRequest
        @param headers: FlightItineraryScanQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightItineraryScanQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.bill_date):
            query['bill_date'] = request.bill_date
        if not UtilClient.is_unset(request.bill_id):
            query['bill_id'] = request.bill_id
        if not UtilClient.is_unset(request.invoice_sub_task_id):
            query['invoice_sub_task_id'] = request.invoice_sub_task_id
        if not UtilClient.is_unset(request.itinerary_num):
            query['itinerary_num'] = request.itinerary_num
        if not UtilClient.is_unset(request.page_no):
            query['page_no'] = request.page_no
        if not UtilClient.is_unset(request.page_size):
            query['page_size'] = request.page_size
        if not UtilClient.is_unset(request.ticket_no):
            query['ticket_no'] = request.ticket_no
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='FlightItineraryScanQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/scan/v1/flight-itinerary',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightItineraryScanQueryResponse(),
            self.call_api(params, req, runtime)
        )

    async def flight_itinerary_scan_query_with_options_async(
        self,
        request: btrip_open_20220520_models.FlightItineraryScanQueryRequest,
        headers: btrip_open_20220520_models.FlightItineraryScanQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightItineraryScanQueryResponse:
        """
        @summary 查询机票行程单扫描件
        
        @param request: FlightItineraryScanQueryRequest
        @param headers: FlightItineraryScanQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightItineraryScanQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.bill_date):
            query['bill_date'] = request.bill_date
        if not UtilClient.is_unset(request.bill_id):
            query['bill_id'] = request.bill_id
        if not UtilClient.is_unset(request.invoice_sub_task_id):
            query['invoice_sub_task_id'] = request.invoice_sub_task_id
        if not UtilClient.is_unset(request.itinerary_num):
            query['itinerary_num'] = request.itinerary_num
        if not UtilClient.is_unset(request.page_no):
            query['page_no'] = request.page_no
        if not UtilClient.is_unset(request.page_size):
            query['page_size'] = request.page_size
        if not UtilClient.is_unset(request.ticket_no):
            query['ticket_no'] = request.ticket_no
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='FlightItineraryScanQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/scan/v1/flight-itinerary',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightItineraryScanQueryResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def flight_itinerary_scan_query(
        self,
        request: btrip_open_20220520_models.FlightItineraryScanQueryRequest,
    ) -> btrip_open_20220520_models.FlightItineraryScanQueryResponse:
        """
        @summary 查询机票行程单扫描件
        
        @param request: FlightItineraryScanQueryRequest
        @return: FlightItineraryScanQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightItineraryScanQueryHeaders()
        return self.flight_itinerary_scan_query_with_options(request, headers, runtime)

    async def flight_itinerary_scan_query_async(
        self,
        request: btrip_open_20220520_models.FlightItineraryScanQueryRequest,
    ) -> btrip_open_20220520_models.FlightItineraryScanQueryResponse:
        """
        @summary 查询机票行程单扫描件
        
        @param request: FlightItineraryScanQueryRequest
        @return: FlightItineraryScanQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightItineraryScanQueryHeaders()
        return await self.flight_itinerary_scan_query_with_options_async(request, headers, runtime)

    def flight_listing_search_with_options(
        self,
        request: btrip_open_20220520_models.FlightListingSearchRequest,
        headers: btrip_open_20220520_models.FlightListingSearchHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightListingSearchResponse:
        """
        @summary 航班列表搜索
        
        @param request: FlightListingSearchRequest
        @param headers: FlightListingSearchHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightListingSearchResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.airline_code):
            query['airline_code'] = request.airline_code
        if not UtilClient.is_unset(request.arr_city_code):
            query['arr_city_code'] = request.arr_city_code
        if not UtilClient.is_unset(request.cabin_class):
            query['cabin_class'] = request.cabin_class
        if not UtilClient.is_unset(request.dep_city_code):
            query['dep_city_code'] = request.dep_city_code
        if not UtilClient.is_unset(request.dep_date):
            query['dep_date'] = request.dep_date
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='FlightListingSearch',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v1/flight/action/listing-search',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightListingSearchResponse(),
            self.call_api(params, req, runtime)
        )

    async def flight_listing_search_with_options_async(
        self,
        request: btrip_open_20220520_models.FlightListingSearchRequest,
        headers: btrip_open_20220520_models.FlightListingSearchHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightListingSearchResponse:
        """
        @summary 航班列表搜索
        
        @param request: FlightListingSearchRequest
        @param headers: FlightListingSearchHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightListingSearchResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.airline_code):
            query['airline_code'] = request.airline_code
        if not UtilClient.is_unset(request.arr_city_code):
            query['arr_city_code'] = request.arr_city_code
        if not UtilClient.is_unset(request.cabin_class):
            query['cabin_class'] = request.cabin_class
        if not UtilClient.is_unset(request.dep_city_code):
            query['dep_city_code'] = request.dep_city_code
        if not UtilClient.is_unset(request.dep_date):
            query['dep_date'] = request.dep_date
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='FlightListingSearch',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v1/flight/action/listing-search',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightListingSearchResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def flight_listing_search(
        self,
        request: btrip_open_20220520_models.FlightListingSearchRequest,
    ) -> btrip_open_20220520_models.FlightListingSearchResponse:
        """
        @summary 航班列表搜索
        
        @param request: FlightListingSearchRequest
        @return: FlightListingSearchResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightListingSearchHeaders()
        return self.flight_listing_search_with_options(request, headers, runtime)

    async def flight_listing_search_async(
        self,
        request: btrip_open_20220520_models.FlightListingSearchRequest,
    ) -> btrip_open_20220520_models.FlightListingSearchResponse:
        """
        @summary 航班列表搜索
        
        @param request: FlightListingSearchRequest
        @return: FlightListingSearchResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightListingSearchHeaders()
        return await self.flight_listing_search_with_options_async(request, headers, runtime)

    def flight_listing_search_v2with_options(
        self,
        tmp_req: btrip_open_20220520_models.FlightListingSearchV2Request,
        headers: btrip_open_20220520_models.FlightListingSearchV2Headers,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightListingSearchV2Response:
        """
        @summary 航班列表搜索
        
        @param tmp_req: FlightListingSearchV2Request
        @param headers: FlightListingSearchV2Headers
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightListingSearchV2Response
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.FlightListingSearchV2ShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.cabin_type_list):
            request.cabin_type_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.cabin_type_list, 'cabin_type_list', 'json')
        if not UtilClient.is_unset(tmp_req.search_journeys):
            request.search_journeys_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.search_journeys, 'search_journeys', 'json')
        query = {}
        if not UtilClient.is_unset(request.airline_code):
            query['airline_code'] = request.airline_code
        if not UtilClient.is_unset(request.cabin_type_list_shrink):
            query['cabin_type_list'] = request.cabin_type_list_shrink
        if not UtilClient.is_unset(request.direct_only):
            query['direct_only'] = request.direct_only
        if not UtilClient.is_unset(request.isv_name):
            query['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.need_multi_class_price):
            query['need_multi_class_price'] = request.need_multi_class_price
        if not UtilClient.is_unset(request.need_query_service_fee):
            query['need_query_service_fee'] = request.need_query_service_fee
        if not UtilClient.is_unset(request.need_share_flight):
            query['need_share_flight'] = request.need_share_flight
        if not UtilClient.is_unset(request.need_ycbest_price):
            query['need_y_c_best_price'] = request.need_ycbest_price
        if not UtilClient.is_unset(request.search_journeys_shrink):
            query['search_journeys'] = request.search_journeys_shrink
        if not UtilClient.is_unset(request.search_mode):
            query['search_mode'] = request.search_mode
        if not UtilClient.is_unset(request.trip_type):
            query['trip_type'] = request.trip_type
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='FlightListingSearchV2',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v2/flight/action/listing-search',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightListingSearchV2Response(),
            self.call_api(params, req, runtime)
        )

    async def flight_listing_search_v2with_options_async(
        self,
        tmp_req: btrip_open_20220520_models.FlightListingSearchV2Request,
        headers: btrip_open_20220520_models.FlightListingSearchV2Headers,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightListingSearchV2Response:
        """
        @summary 航班列表搜索
        
        @param tmp_req: FlightListingSearchV2Request
        @param headers: FlightListingSearchV2Headers
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightListingSearchV2Response
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.FlightListingSearchV2ShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.cabin_type_list):
            request.cabin_type_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.cabin_type_list, 'cabin_type_list', 'json')
        if not UtilClient.is_unset(tmp_req.search_journeys):
            request.search_journeys_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.search_journeys, 'search_journeys', 'json')
        query = {}
        if not UtilClient.is_unset(request.airline_code):
            query['airline_code'] = request.airline_code
        if not UtilClient.is_unset(request.cabin_type_list_shrink):
            query['cabin_type_list'] = request.cabin_type_list_shrink
        if not UtilClient.is_unset(request.direct_only):
            query['direct_only'] = request.direct_only
        if not UtilClient.is_unset(request.isv_name):
            query['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.need_multi_class_price):
            query['need_multi_class_price'] = request.need_multi_class_price
        if not UtilClient.is_unset(request.need_query_service_fee):
            query['need_query_service_fee'] = request.need_query_service_fee
        if not UtilClient.is_unset(request.need_share_flight):
            query['need_share_flight'] = request.need_share_flight
        if not UtilClient.is_unset(request.need_ycbest_price):
            query['need_y_c_best_price'] = request.need_ycbest_price
        if not UtilClient.is_unset(request.search_journeys_shrink):
            query['search_journeys'] = request.search_journeys_shrink
        if not UtilClient.is_unset(request.search_mode):
            query['search_mode'] = request.search_mode
        if not UtilClient.is_unset(request.trip_type):
            query['trip_type'] = request.trip_type
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='FlightListingSearchV2',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v2/flight/action/listing-search',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightListingSearchV2Response(),
            await self.call_api_async(params, req, runtime)
        )

    def flight_listing_search_v2(
        self,
        request: btrip_open_20220520_models.FlightListingSearchV2Request,
    ) -> btrip_open_20220520_models.FlightListingSearchV2Response:
        """
        @summary 航班列表搜索
        
        @param request: FlightListingSearchV2Request
        @return: FlightListingSearchV2Response
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightListingSearchV2Headers()
        return self.flight_listing_search_v2with_options(request, headers, runtime)

    async def flight_listing_search_v2_async(
        self,
        request: btrip_open_20220520_models.FlightListingSearchV2Request,
    ) -> btrip_open_20220520_models.FlightListingSearchV2Response:
        """
        @summary 航班列表搜索
        
        @param request: FlightListingSearchV2Request
        @return: FlightListingSearchV2Response
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightListingSearchV2Headers()
        return await self.flight_listing_search_v2with_options_async(request, headers, runtime)

    def flight_modify_apply_v2with_options(
        self,
        tmp_req: btrip_open_20220520_models.FlightModifyApplyV2Request,
        headers: btrip_open_20220520_models.FlightModifyApplyV2Headers,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightModifyApplyV2Response:
        """
        @summary 机票改签申请
        
        @param tmp_req: FlightModifyApplyV2Request
        @param headers: FlightModifyApplyV2Headers
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightModifyApplyV2Response
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.FlightModifyApplyV2ShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.passenger_segment_relations):
            request.passenger_segment_relations_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.passenger_segment_relations, 'passenger_segment_relations', 'json')
        body = {}
        if not UtilClient.is_unset(request.cache_key):
            body['cache_key'] = request.cache_key
        if not UtilClient.is_unset(request.contact_phone):
            body['contact_phone'] = request.contact_phone
        if not UtilClient.is_unset(request.isv_name):
            body['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.item_id):
            body['item_id'] = request.item_id
        if not UtilClient.is_unset(request.order_id):
            body['order_id'] = request.order_id
        if not UtilClient.is_unset(request.out_order_id):
            body['out_order_id'] = request.out_order_id
        if not UtilClient.is_unset(request.out_sub_order_id):
            body['out_sub_order_id'] = request.out_sub_order_id
        if not UtilClient.is_unset(request.passenger_segment_relations_shrink):
            body['passenger_segment_relations'] = request.passenger_segment_relations_shrink
        if not UtilClient.is_unset(request.reason):
            body['reason'] = request.reason
        if not UtilClient.is_unset(request.session_id):
            body['session_id'] = request.session_id
        if not UtilClient.is_unset(request.voluntary):
            body['voluntary'] = request.voluntary
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='FlightModifyApplyV2',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v2/modify/action/apply',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightModifyApplyV2Response(),
            self.call_api(params, req, runtime)
        )

    async def flight_modify_apply_v2with_options_async(
        self,
        tmp_req: btrip_open_20220520_models.FlightModifyApplyV2Request,
        headers: btrip_open_20220520_models.FlightModifyApplyV2Headers,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightModifyApplyV2Response:
        """
        @summary 机票改签申请
        
        @param tmp_req: FlightModifyApplyV2Request
        @param headers: FlightModifyApplyV2Headers
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightModifyApplyV2Response
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.FlightModifyApplyV2ShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.passenger_segment_relations):
            request.passenger_segment_relations_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.passenger_segment_relations, 'passenger_segment_relations', 'json')
        body = {}
        if not UtilClient.is_unset(request.cache_key):
            body['cache_key'] = request.cache_key
        if not UtilClient.is_unset(request.contact_phone):
            body['contact_phone'] = request.contact_phone
        if not UtilClient.is_unset(request.isv_name):
            body['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.item_id):
            body['item_id'] = request.item_id
        if not UtilClient.is_unset(request.order_id):
            body['order_id'] = request.order_id
        if not UtilClient.is_unset(request.out_order_id):
            body['out_order_id'] = request.out_order_id
        if not UtilClient.is_unset(request.out_sub_order_id):
            body['out_sub_order_id'] = request.out_sub_order_id
        if not UtilClient.is_unset(request.passenger_segment_relations_shrink):
            body['passenger_segment_relations'] = request.passenger_segment_relations_shrink
        if not UtilClient.is_unset(request.reason):
            body['reason'] = request.reason
        if not UtilClient.is_unset(request.session_id):
            body['session_id'] = request.session_id
        if not UtilClient.is_unset(request.voluntary):
            body['voluntary'] = request.voluntary
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='FlightModifyApplyV2',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v2/modify/action/apply',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightModifyApplyV2Response(),
            await self.call_api_async(params, req, runtime)
        )

    def flight_modify_apply_v2(
        self,
        request: btrip_open_20220520_models.FlightModifyApplyV2Request,
    ) -> btrip_open_20220520_models.FlightModifyApplyV2Response:
        """
        @summary 机票改签申请
        
        @param request: FlightModifyApplyV2Request
        @return: FlightModifyApplyV2Response
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightModifyApplyV2Headers()
        return self.flight_modify_apply_v2with_options(request, headers, runtime)

    async def flight_modify_apply_v2_async(
        self,
        request: btrip_open_20220520_models.FlightModifyApplyV2Request,
    ) -> btrip_open_20220520_models.FlightModifyApplyV2Response:
        """
        @summary 机票改签申请
        
        @param request: FlightModifyApplyV2Request
        @return: FlightModifyApplyV2Response
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightModifyApplyV2Headers()
        return await self.flight_modify_apply_v2with_options_async(request, headers, runtime)

    def flight_modify_cancel_v2with_options(
        self,
        request: btrip_open_20220520_models.FlightModifyCancelV2Request,
        headers: btrip_open_20220520_models.FlightModifyCancelV2Headers,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightModifyCancelV2Response:
        """
        @summary 机票改签取消
        
        @param request: FlightModifyCancelV2Request
        @param headers: FlightModifyCancelV2Headers
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightModifyCancelV2Response
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.isv_name):
            query['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.order_id):
            query['order_id'] = request.order_id
        if not UtilClient.is_unset(request.out_order_id):
            query['out_order_id'] = request.out_order_id
        if not UtilClient.is_unset(request.out_sub_order_id):
            query['out_sub_order_id'] = request.out_sub_order_id
        if not UtilClient.is_unset(request.sub_order_id):
            query['sub_order_id'] = request.sub_order_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='FlightModifyCancelV2',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v2/modify/action/cancel',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightModifyCancelV2Response(),
            self.call_api(params, req, runtime)
        )

    async def flight_modify_cancel_v2with_options_async(
        self,
        request: btrip_open_20220520_models.FlightModifyCancelV2Request,
        headers: btrip_open_20220520_models.FlightModifyCancelV2Headers,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightModifyCancelV2Response:
        """
        @summary 机票改签取消
        
        @param request: FlightModifyCancelV2Request
        @param headers: FlightModifyCancelV2Headers
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightModifyCancelV2Response
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.isv_name):
            query['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.order_id):
            query['order_id'] = request.order_id
        if not UtilClient.is_unset(request.out_order_id):
            query['out_order_id'] = request.out_order_id
        if not UtilClient.is_unset(request.out_sub_order_id):
            query['out_sub_order_id'] = request.out_sub_order_id
        if not UtilClient.is_unset(request.sub_order_id):
            query['sub_order_id'] = request.sub_order_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='FlightModifyCancelV2',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v2/modify/action/cancel',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightModifyCancelV2Response(),
            await self.call_api_async(params, req, runtime)
        )

    def flight_modify_cancel_v2(
        self,
        request: btrip_open_20220520_models.FlightModifyCancelV2Request,
    ) -> btrip_open_20220520_models.FlightModifyCancelV2Response:
        """
        @summary 机票改签取消
        
        @param request: FlightModifyCancelV2Request
        @return: FlightModifyCancelV2Response
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightModifyCancelV2Headers()
        return self.flight_modify_cancel_v2with_options(request, headers, runtime)

    async def flight_modify_cancel_v2_async(
        self,
        request: btrip_open_20220520_models.FlightModifyCancelV2Request,
    ) -> btrip_open_20220520_models.FlightModifyCancelV2Response:
        """
        @summary 机票改签取消
        
        @param request: FlightModifyCancelV2Request
        @return: FlightModifyCancelV2Response
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightModifyCancelV2Headers()
        return await self.flight_modify_cancel_v2with_options_async(request, headers, runtime)

    def flight_modify_listing_search_v2with_options(
        self,
        tmp_req: btrip_open_20220520_models.FlightModifyListingSearchV2Request,
        headers: btrip_open_20220520_models.FlightModifyListingSearchV2Headers,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightModifyListingSearchV2Response:
        """
        @summary 机票改签列表搜索
        
        @param tmp_req: FlightModifyListingSearchV2Request
        @param headers: FlightModifyListingSearchV2Headers
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightModifyListingSearchV2Response
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.FlightModifyListingSearchV2ShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.cabin_class):
            request.cabin_class_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.cabin_class, 'cabin_class', 'json')
        if not UtilClient.is_unset(tmp_req.dep_date):
            request.dep_date_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.dep_date, 'dep_date', 'json')
        if not UtilClient.is_unset(tmp_req.passenger_segment_relations):
            request.passenger_segment_relations_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.passenger_segment_relations, 'passenger_segment_relations', 'json')
        if not UtilClient.is_unset(tmp_req.selected_segments):
            request.selected_segments_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.selected_segments, 'selected_segments', 'json')
        query = {}
        if not UtilClient.is_unset(request.cabin_class_shrink):
            query['cabin_class'] = request.cabin_class_shrink
        if not UtilClient.is_unset(request.dep_date_shrink):
            query['dep_date'] = request.dep_date_shrink
        if not UtilClient.is_unset(request.interface_caller_is_support_retry):
            query['interface_caller_is_support_retry'] = request.interface_caller_is_support_retry
        if not UtilClient.is_unset(request.isv_name):
            query['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.order_id):
            query['order_id'] = request.order_id
        if not UtilClient.is_unset(request.out_order_id):
            query['out_order_id'] = request.out_order_id
        if not UtilClient.is_unset(request.passenger_segment_relations_shrink):
            query['passenger_segment_relations'] = request.passenger_segment_relations_shrink
        if not UtilClient.is_unset(request.search_mode):
            query['search_mode'] = request.search_mode
        if not UtilClient.is_unset(request.search_retry_token):
            query['search_retry_token'] = request.search_retry_token
        if not UtilClient.is_unset(request.selected_segments_shrink):
            query['selected_segments'] = request.selected_segments_shrink
        if not UtilClient.is_unset(request.session_id):
            query['session_id'] = request.session_id
        if not UtilClient.is_unset(request.voluntary):
            query['voluntary'] = request.voluntary
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='FlightModifyListingSearchV2',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v2/modify/action/listing-search',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightModifyListingSearchV2Response(),
            self.call_api(params, req, runtime)
        )

    async def flight_modify_listing_search_v2with_options_async(
        self,
        tmp_req: btrip_open_20220520_models.FlightModifyListingSearchV2Request,
        headers: btrip_open_20220520_models.FlightModifyListingSearchV2Headers,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightModifyListingSearchV2Response:
        """
        @summary 机票改签列表搜索
        
        @param tmp_req: FlightModifyListingSearchV2Request
        @param headers: FlightModifyListingSearchV2Headers
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightModifyListingSearchV2Response
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.FlightModifyListingSearchV2ShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.cabin_class):
            request.cabin_class_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.cabin_class, 'cabin_class', 'json')
        if not UtilClient.is_unset(tmp_req.dep_date):
            request.dep_date_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.dep_date, 'dep_date', 'json')
        if not UtilClient.is_unset(tmp_req.passenger_segment_relations):
            request.passenger_segment_relations_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.passenger_segment_relations, 'passenger_segment_relations', 'json')
        if not UtilClient.is_unset(tmp_req.selected_segments):
            request.selected_segments_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.selected_segments, 'selected_segments', 'json')
        query = {}
        if not UtilClient.is_unset(request.cabin_class_shrink):
            query['cabin_class'] = request.cabin_class_shrink
        if not UtilClient.is_unset(request.dep_date_shrink):
            query['dep_date'] = request.dep_date_shrink
        if not UtilClient.is_unset(request.interface_caller_is_support_retry):
            query['interface_caller_is_support_retry'] = request.interface_caller_is_support_retry
        if not UtilClient.is_unset(request.isv_name):
            query['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.order_id):
            query['order_id'] = request.order_id
        if not UtilClient.is_unset(request.out_order_id):
            query['out_order_id'] = request.out_order_id
        if not UtilClient.is_unset(request.passenger_segment_relations_shrink):
            query['passenger_segment_relations'] = request.passenger_segment_relations_shrink
        if not UtilClient.is_unset(request.search_mode):
            query['search_mode'] = request.search_mode
        if not UtilClient.is_unset(request.search_retry_token):
            query['search_retry_token'] = request.search_retry_token
        if not UtilClient.is_unset(request.selected_segments_shrink):
            query['selected_segments'] = request.selected_segments_shrink
        if not UtilClient.is_unset(request.session_id):
            query['session_id'] = request.session_id
        if not UtilClient.is_unset(request.voluntary):
            query['voluntary'] = request.voluntary
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='FlightModifyListingSearchV2',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v2/modify/action/listing-search',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightModifyListingSearchV2Response(),
            await self.call_api_async(params, req, runtime)
        )

    def flight_modify_listing_search_v2(
        self,
        request: btrip_open_20220520_models.FlightModifyListingSearchV2Request,
    ) -> btrip_open_20220520_models.FlightModifyListingSearchV2Response:
        """
        @summary 机票改签列表搜索
        
        @param request: FlightModifyListingSearchV2Request
        @return: FlightModifyListingSearchV2Response
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightModifyListingSearchV2Headers()
        return self.flight_modify_listing_search_v2with_options(request, headers, runtime)

    async def flight_modify_listing_search_v2_async(
        self,
        request: btrip_open_20220520_models.FlightModifyListingSearchV2Request,
    ) -> btrip_open_20220520_models.FlightModifyListingSearchV2Response:
        """
        @summary 机票改签列表搜索
        
        @param request: FlightModifyListingSearchV2Request
        @return: FlightModifyListingSearchV2Response
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightModifyListingSearchV2Headers()
        return await self.flight_modify_listing_search_v2with_options_async(request, headers, runtime)

    def flight_modify_order_detail_v2with_options(
        self,
        request: btrip_open_20220520_models.FlightModifyOrderDetailV2Request,
        headers: btrip_open_20220520_models.FlightModifyOrderDetailV2Headers,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightModifyOrderDetailV2Response:
        """
        @summary 机票改签详情
        
        @param request: FlightModifyOrderDetailV2Request
        @param headers: FlightModifyOrderDetailV2Headers
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightModifyOrderDetailV2Response
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.isv_name):
            query['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.modify_apply_id):
            query['modify_apply_id'] = request.modify_apply_id
        if not UtilClient.is_unset(request.need_query_service_fee):
            query['need_query_service_fee'] = request.need_query_service_fee
        if not UtilClient.is_unset(request.order_id):
            query['order_id'] = request.order_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='FlightModifyOrderDetailV2',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v2/modify/action/detail',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightModifyOrderDetailV2Response(),
            self.call_api(params, req, runtime)
        )

    async def flight_modify_order_detail_v2with_options_async(
        self,
        request: btrip_open_20220520_models.FlightModifyOrderDetailV2Request,
        headers: btrip_open_20220520_models.FlightModifyOrderDetailV2Headers,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightModifyOrderDetailV2Response:
        """
        @summary 机票改签详情
        
        @param request: FlightModifyOrderDetailV2Request
        @param headers: FlightModifyOrderDetailV2Headers
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightModifyOrderDetailV2Response
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.isv_name):
            query['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.modify_apply_id):
            query['modify_apply_id'] = request.modify_apply_id
        if not UtilClient.is_unset(request.need_query_service_fee):
            query['need_query_service_fee'] = request.need_query_service_fee
        if not UtilClient.is_unset(request.order_id):
            query['order_id'] = request.order_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='FlightModifyOrderDetailV2',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v2/modify/action/detail',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightModifyOrderDetailV2Response(),
            await self.call_api_async(params, req, runtime)
        )

    def flight_modify_order_detail_v2(
        self,
        request: btrip_open_20220520_models.FlightModifyOrderDetailV2Request,
    ) -> btrip_open_20220520_models.FlightModifyOrderDetailV2Response:
        """
        @summary 机票改签详情
        
        @param request: FlightModifyOrderDetailV2Request
        @return: FlightModifyOrderDetailV2Response
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightModifyOrderDetailV2Headers()
        return self.flight_modify_order_detail_v2with_options(request, headers, runtime)

    async def flight_modify_order_detail_v2_async(
        self,
        request: btrip_open_20220520_models.FlightModifyOrderDetailV2Request,
    ) -> btrip_open_20220520_models.FlightModifyOrderDetailV2Response:
        """
        @summary 机票改签详情
        
        @param request: FlightModifyOrderDetailV2Request
        @return: FlightModifyOrderDetailV2Response
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightModifyOrderDetailV2Headers()
        return await self.flight_modify_order_detail_v2with_options_async(request, headers, runtime)

    def flight_modify_ota_search_v2with_options(
        self,
        tmp_req: btrip_open_20220520_models.FlightModifyOtaSearchV2Request,
        headers: btrip_open_20220520_models.FlightModifyOtaSearchV2Headers,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightModifyOtaSearchV2Response:
        """
        @summary 机票改签报价搜索
        
        @param tmp_req: FlightModifyOtaSearchV2Request
        @param headers: FlightModifyOtaSearchV2Headers
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightModifyOtaSearchV2Response
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.FlightModifyOtaSearchV2ShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.cabin_class):
            request.cabin_class_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.cabin_class, 'cabin_class', 'json')
        if not UtilClient.is_unset(tmp_req.dep_date):
            request.dep_date_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.dep_date, 'dep_date', 'json')
        if not UtilClient.is_unset(tmp_req.passenger_segment_relations):
            request.passenger_segment_relations_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.passenger_segment_relations, 'passenger_segment_relations', 'json')
        if not UtilClient.is_unset(tmp_req.selected_segments):
            request.selected_segments_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.selected_segments, 'selected_segments', 'json')
        query = {}
        if not UtilClient.is_unset(request.cabin_class_shrink):
            query['cabin_class'] = request.cabin_class_shrink
        if not UtilClient.is_unset(request.dep_date_shrink):
            query['dep_date'] = request.dep_date_shrink
        if not UtilClient.is_unset(request.isv_name):
            query['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.order_id):
            query['order_id'] = request.order_id
        if not UtilClient.is_unset(request.out_order_id):
            query['out_order_id'] = request.out_order_id
        if not UtilClient.is_unset(request.passenger_segment_relations_shrink):
            query['passenger_segment_relations'] = request.passenger_segment_relations_shrink
        if not UtilClient.is_unset(request.selected_segments_shrink):
            query['selected_segments'] = request.selected_segments_shrink
        if not UtilClient.is_unset(request.session_id):
            query['session_id'] = request.session_id
        if not UtilClient.is_unset(request.voluntary):
            query['voluntary'] = request.voluntary
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='FlightModifyOtaSearchV2',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v2/modify/action/ota-search',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightModifyOtaSearchV2Response(),
            self.call_api(params, req, runtime)
        )

    async def flight_modify_ota_search_v2with_options_async(
        self,
        tmp_req: btrip_open_20220520_models.FlightModifyOtaSearchV2Request,
        headers: btrip_open_20220520_models.FlightModifyOtaSearchV2Headers,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightModifyOtaSearchV2Response:
        """
        @summary 机票改签报价搜索
        
        @param tmp_req: FlightModifyOtaSearchV2Request
        @param headers: FlightModifyOtaSearchV2Headers
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightModifyOtaSearchV2Response
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.FlightModifyOtaSearchV2ShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.cabin_class):
            request.cabin_class_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.cabin_class, 'cabin_class', 'json')
        if not UtilClient.is_unset(tmp_req.dep_date):
            request.dep_date_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.dep_date, 'dep_date', 'json')
        if not UtilClient.is_unset(tmp_req.passenger_segment_relations):
            request.passenger_segment_relations_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.passenger_segment_relations, 'passenger_segment_relations', 'json')
        if not UtilClient.is_unset(tmp_req.selected_segments):
            request.selected_segments_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.selected_segments, 'selected_segments', 'json')
        query = {}
        if not UtilClient.is_unset(request.cabin_class_shrink):
            query['cabin_class'] = request.cabin_class_shrink
        if not UtilClient.is_unset(request.dep_date_shrink):
            query['dep_date'] = request.dep_date_shrink
        if not UtilClient.is_unset(request.isv_name):
            query['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.order_id):
            query['order_id'] = request.order_id
        if not UtilClient.is_unset(request.out_order_id):
            query['out_order_id'] = request.out_order_id
        if not UtilClient.is_unset(request.passenger_segment_relations_shrink):
            query['passenger_segment_relations'] = request.passenger_segment_relations_shrink
        if not UtilClient.is_unset(request.selected_segments_shrink):
            query['selected_segments'] = request.selected_segments_shrink
        if not UtilClient.is_unset(request.session_id):
            query['session_id'] = request.session_id
        if not UtilClient.is_unset(request.voluntary):
            query['voluntary'] = request.voluntary
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='FlightModifyOtaSearchV2',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v2/modify/action/ota-search',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightModifyOtaSearchV2Response(),
            await self.call_api_async(params, req, runtime)
        )

    def flight_modify_ota_search_v2(
        self,
        request: btrip_open_20220520_models.FlightModifyOtaSearchV2Request,
    ) -> btrip_open_20220520_models.FlightModifyOtaSearchV2Response:
        """
        @summary 机票改签报价搜索
        
        @param request: FlightModifyOtaSearchV2Request
        @return: FlightModifyOtaSearchV2Response
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightModifyOtaSearchV2Headers()
        return self.flight_modify_ota_search_v2with_options(request, headers, runtime)

    async def flight_modify_ota_search_v2_async(
        self,
        request: btrip_open_20220520_models.FlightModifyOtaSearchV2Request,
    ) -> btrip_open_20220520_models.FlightModifyOtaSearchV2Response:
        """
        @summary 机票改签报价搜索
        
        @param request: FlightModifyOtaSearchV2Request
        @return: FlightModifyOtaSearchV2Response
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightModifyOtaSearchV2Headers()
        return await self.flight_modify_ota_search_v2with_options_async(request, headers, runtime)

    def flight_modify_pay_v2with_options(
        self,
        tmp_req: btrip_open_20220520_models.FlightModifyPayV2Request,
        headers: btrip_open_20220520_models.FlightModifyPayV2Headers,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightModifyPayV2Response:
        """
        @summary 机票改签支付
        
        @param tmp_req: FlightModifyPayV2Request
        @param headers: FlightModifyPayV2Headers
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightModifyPayV2Response
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.FlightModifyPayV2ShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.ext_params):
            request.ext_params_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.ext_params, 'ext_params', 'json')
        body = {}
        if not UtilClient.is_unset(request.ext_params_shrink):
            body['ext_params'] = request.ext_params_shrink
        if not UtilClient.is_unset(request.isv_name):
            body['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.modify_pay_amount):
            body['modify_pay_amount'] = request.modify_pay_amount
        if not UtilClient.is_unset(request.order_id):
            body['order_id'] = request.order_id
        if not UtilClient.is_unset(request.out_order_id):
            body['out_order_id'] = request.out_order_id
        if not UtilClient.is_unset(request.out_sub_order_id):
            body['out_sub_order_id'] = request.out_sub_order_id
        if not UtilClient.is_unset(request.sub_order_id):
            body['sub_order_id'] = request.sub_order_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='FlightModifyPayV2',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v2/modify/action/pay',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightModifyPayV2Response(),
            self.call_api(params, req, runtime)
        )

    async def flight_modify_pay_v2with_options_async(
        self,
        tmp_req: btrip_open_20220520_models.FlightModifyPayV2Request,
        headers: btrip_open_20220520_models.FlightModifyPayV2Headers,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightModifyPayV2Response:
        """
        @summary 机票改签支付
        
        @param tmp_req: FlightModifyPayV2Request
        @param headers: FlightModifyPayV2Headers
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightModifyPayV2Response
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.FlightModifyPayV2ShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.ext_params):
            request.ext_params_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.ext_params, 'ext_params', 'json')
        body = {}
        if not UtilClient.is_unset(request.ext_params_shrink):
            body['ext_params'] = request.ext_params_shrink
        if not UtilClient.is_unset(request.isv_name):
            body['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.modify_pay_amount):
            body['modify_pay_amount'] = request.modify_pay_amount
        if not UtilClient.is_unset(request.order_id):
            body['order_id'] = request.order_id
        if not UtilClient.is_unset(request.out_order_id):
            body['out_order_id'] = request.out_order_id
        if not UtilClient.is_unset(request.out_sub_order_id):
            body['out_sub_order_id'] = request.out_sub_order_id
        if not UtilClient.is_unset(request.sub_order_id):
            body['sub_order_id'] = request.sub_order_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='FlightModifyPayV2',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v2/modify/action/pay',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightModifyPayV2Response(),
            await self.call_api_async(params, req, runtime)
        )

    def flight_modify_pay_v2(
        self,
        request: btrip_open_20220520_models.FlightModifyPayV2Request,
    ) -> btrip_open_20220520_models.FlightModifyPayV2Response:
        """
        @summary 机票改签支付
        
        @param request: FlightModifyPayV2Request
        @return: FlightModifyPayV2Response
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightModifyPayV2Headers()
        return self.flight_modify_pay_v2with_options(request, headers, runtime)

    async def flight_modify_pay_v2_async(
        self,
        request: btrip_open_20220520_models.FlightModifyPayV2Request,
    ) -> btrip_open_20220520_models.FlightModifyPayV2Response:
        """
        @summary 机票改签支付
        
        @param request: FlightModifyPayV2Request
        @return: FlightModifyPayV2Response
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightModifyPayV2Headers()
        return await self.flight_modify_pay_v2with_options_async(request, headers, runtime)

    def flight_order_detail_info_with_options(
        self,
        request: btrip_open_20220520_models.FlightOrderDetailInfoRequest,
        headers: btrip_open_20220520_models.FlightOrderDetailInfoHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightOrderDetailInfoResponse:
        """
        @summary 航班订单明细信息
        
        @param request: FlightOrderDetailInfoRequest
        @param headers: FlightOrderDetailInfoHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightOrderDetailInfoResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.dis_order_id):
            query['dis_order_id'] = request.dis_order_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='FlightOrderDetailInfo',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v1/order/action/detail',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightOrderDetailInfoResponse(),
            self.call_api(params, req, runtime)
        )

    async def flight_order_detail_info_with_options_async(
        self,
        request: btrip_open_20220520_models.FlightOrderDetailInfoRequest,
        headers: btrip_open_20220520_models.FlightOrderDetailInfoHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightOrderDetailInfoResponse:
        """
        @summary 航班订单明细信息
        
        @param request: FlightOrderDetailInfoRequest
        @param headers: FlightOrderDetailInfoHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightOrderDetailInfoResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.dis_order_id):
            query['dis_order_id'] = request.dis_order_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='FlightOrderDetailInfo',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v1/order/action/detail',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightOrderDetailInfoResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def flight_order_detail_info(
        self,
        request: btrip_open_20220520_models.FlightOrderDetailInfoRequest,
    ) -> btrip_open_20220520_models.FlightOrderDetailInfoResponse:
        """
        @summary 航班订单明细信息
        
        @param request: FlightOrderDetailInfoRequest
        @return: FlightOrderDetailInfoResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightOrderDetailInfoHeaders()
        return self.flight_order_detail_info_with_options(request, headers, runtime)

    async def flight_order_detail_info_async(
        self,
        request: btrip_open_20220520_models.FlightOrderDetailInfoRequest,
    ) -> btrip_open_20220520_models.FlightOrderDetailInfoResponse:
        """
        @summary 航班订单明细信息
        
        @param request: FlightOrderDetailInfoRequest
        @return: FlightOrderDetailInfoResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightOrderDetailInfoHeaders()
        return await self.flight_order_detail_info_with_options_async(request, headers, runtime)

    def flight_order_detail_v2with_options(
        self,
        request: btrip_open_20220520_models.FlightOrderDetailV2Request,
        headers: btrip_open_20220520_models.FlightOrderDetailV2Headers,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightOrderDetailV2Response:
        """
        @summary 机票订单详情
        
        @param request: FlightOrderDetailV2Request
        @param headers: FlightOrderDetailV2Headers
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightOrderDetailV2Response
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.isv_name):
            query['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.order_id):
            query['order_id'] = request.order_id
        if not UtilClient.is_unset(request.out_order_id):
            query['out_order_id'] = request.out_order_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='FlightOrderDetailV2',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v2/order/action/detail',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightOrderDetailV2Response(),
            self.call_api(params, req, runtime)
        )

    async def flight_order_detail_v2with_options_async(
        self,
        request: btrip_open_20220520_models.FlightOrderDetailV2Request,
        headers: btrip_open_20220520_models.FlightOrderDetailV2Headers,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightOrderDetailV2Response:
        """
        @summary 机票订单详情
        
        @param request: FlightOrderDetailV2Request
        @param headers: FlightOrderDetailV2Headers
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightOrderDetailV2Response
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.isv_name):
            query['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.order_id):
            query['order_id'] = request.order_id
        if not UtilClient.is_unset(request.out_order_id):
            query['out_order_id'] = request.out_order_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='FlightOrderDetailV2',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v2/order/action/detail',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightOrderDetailV2Response(),
            await self.call_api_async(params, req, runtime)
        )

    def flight_order_detail_v2(
        self,
        request: btrip_open_20220520_models.FlightOrderDetailV2Request,
    ) -> btrip_open_20220520_models.FlightOrderDetailV2Response:
        """
        @summary 机票订单详情
        
        @param request: FlightOrderDetailV2Request
        @return: FlightOrderDetailV2Response
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightOrderDetailV2Headers()
        return self.flight_order_detail_v2with_options(request, headers, runtime)

    async def flight_order_detail_v2_async(
        self,
        request: btrip_open_20220520_models.FlightOrderDetailV2Request,
    ) -> btrip_open_20220520_models.FlightOrderDetailV2Response:
        """
        @summary 机票订单详情
        
        @param request: FlightOrderDetailV2Request
        @return: FlightOrderDetailV2Response
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightOrderDetailV2Headers()
        return await self.flight_order_detail_v2with_options_async(request, headers, runtime)

    def flight_order_list_query_with_options(
        self,
        request: btrip_open_20220520_models.FlightOrderListQueryRequest,
        headers: btrip_open_20220520_models.FlightOrderListQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightOrderListQueryResponse:
        """
        @summary 查询机票订单列表
        
        @param request: FlightOrderListQueryRequest
        @param headers: FlightOrderListQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightOrderListQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.all_apply):
            query['all_apply'] = request.all_apply
        if not UtilClient.is_unset(request.apply_id):
            query['apply_id'] = request.apply_id
        if not UtilClient.is_unset(request.depart_id):
            query['depart_id'] = request.depart_id
        if not UtilClient.is_unset(request.end_time):
            query['end_time'] = request.end_time
        if not UtilClient.is_unset(request.page):
            query['page'] = request.page
        if not UtilClient.is_unset(request.page_size):
            query['page_size'] = request.page_size
        if not UtilClient.is_unset(request.start_time):
            query['start_time'] = request.start_time
        if not UtilClient.is_unset(request.thirdpart_apply_id):
            query['thirdpart_apply_id'] = request.thirdpart_apply_id
        if not UtilClient.is_unset(request.update_end_time):
            query['update_end_time'] = request.update_end_time
        if not UtilClient.is_unset(request.update_start_time):
            query['update_start_time'] = request.update_start_time
        if not UtilClient.is_unset(request.user_id):
            query['user_id'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='FlightOrderListQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/flight/v1/order-list',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightOrderListQueryResponse(),
            self.call_api(params, req, runtime)
        )

    async def flight_order_list_query_with_options_async(
        self,
        request: btrip_open_20220520_models.FlightOrderListQueryRequest,
        headers: btrip_open_20220520_models.FlightOrderListQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightOrderListQueryResponse:
        """
        @summary 查询机票订单列表
        
        @param request: FlightOrderListQueryRequest
        @param headers: FlightOrderListQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightOrderListQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.all_apply):
            query['all_apply'] = request.all_apply
        if not UtilClient.is_unset(request.apply_id):
            query['apply_id'] = request.apply_id
        if not UtilClient.is_unset(request.depart_id):
            query['depart_id'] = request.depart_id
        if not UtilClient.is_unset(request.end_time):
            query['end_time'] = request.end_time
        if not UtilClient.is_unset(request.page):
            query['page'] = request.page
        if not UtilClient.is_unset(request.page_size):
            query['page_size'] = request.page_size
        if not UtilClient.is_unset(request.start_time):
            query['start_time'] = request.start_time
        if not UtilClient.is_unset(request.thirdpart_apply_id):
            query['thirdpart_apply_id'] = request.thirdpart_apply_id
        if not UtilClient.is_unset(request.update_end_time):
            query['update_end_time'] = request.update_end_time
        if not UtilClient.is_unset(request.update_start_time):
            query['update_start_time'] = request.update_start_time
        if not UtilClient.is_unset(request.user_id):
            query['user_id'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='FlightOrderListQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/flight/v1/order-list',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightOrderListQueryResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def flight_order_list_query(
        self,
        request: btrip_open_20220520_models.FlightOrderListQueryRequest,
    ) -> btrip_open_20220520_models.FlightOrderListQueryResponse:
        """
        @summary 查询机票订单列表
        
        @param request: FlightOrderListQueryRequest
        @return: FlightOrderListQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightOrderListQueryHeaders()
        return self.flight_order_list_query_with_options(request, headers, runtime)

    async def flight_order_list_query_async(
        self,
        request: btrip_open_20220520_models.FlightOrderListQueryRequest,
    ) -> btrip_open_20220520_models.FlightOrderListQueryResponse:
        """
        @summary 查询机票订单列表
        
        @param request: FlightOrderListQueryRequest
        @return: FlightOrderListQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightOrderListQueryHeaders()
        return await self.flight_order_list_query_with_options_async(request, headers, runtime)

    def flight_order_query_with_options(
        self,
        request: btrip_open_20220520_models.FlightOrderQueryRequest,
        headers: btrip_open_20220520_models.FlightOrderQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightOrderQueryResponse:
        """
        @summary 查询机票订单详情（含票信息）
        
        @param request: FlightOrderQueryRequest
        @param headers: FlightOrderQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightOrderQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.order_id):
            query['order_id'] = request.order_id
        if not UtilClient.is_unset(request.user_id):
            query['user_id'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='FlightOrderQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/flight/v1/order',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightOrderQueryResponse(),
            self.call_api(params, req, runtime)
        )

    async def flight_order_query_with_options_async(
        self,
        request: btrip_open_20220520_models.FlightOrderQueryRequest,
        headers: btrip_open_20220520_models.FlightOrderQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightOrderQueryResponse:
        """
        @summary 查询机票订单详情（含票信息）
        
        @param request: FlightOrderQueryRequest
        @param headers: FlightOrderQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightOrderQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.order_id):
            query['order_id'] = request.order_id
        if not UtilClient.is_unset(request.user_id):
            query['user_id'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='FlightOrderQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/flight/v1/order',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightOrderQueryResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def flight_order_query(
        self,
        request: btrip_open_20220520_models.FlightOrderQueryRequest,
    ) -> btrip_open_20220520_models.FlightOrderQueryResponse:
        """
        @summary 查询机票订单详情（含票信息）
        
        @param request: FlightOrderQueryRequest
        @return: FlightOrderQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightOrderQueryHeaders()
        return self.flight_order_query_with_options(request, headers, runtime)

    async def flight_order_query_async(
        self,
        request: btrip_open_20220520_models.FlightOrderQueryRequest,
    ) -> btrip_open_20220520_models.FlightOrderQueryResponse:
        """
        @summary 查询机票订单详情（含票信息）
        
        @param request: FlightOrderQueryRequest
        @return: FlightOrderQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightOrderQueryHeaders()
        return await self.flight_order_query_with_options_async(request, headers, runtime)

    def flight_ota_item_detail_with_options(
        self,
        request: btrip_open_20220520_models.FlightOtaItemDetailRequest,
        headers: btrip_open_20220520_models.FlightOtaItemDetailHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightOtaItemDetailResponse:
        """
        @summary 查询退改规则行李额
        
        @param request: FlightOtaItemDetailRequest
        @param headers: FlightOtaItemDetailHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightOtaItemDetailResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.isv_name):
            query['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.ota_item_id):
            query['ota_item_id'] = request.ota_item_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='FlightOtaItemDetail',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v1/flight/action/ota-item-detail',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightOtaItemDetailResponse(),
            self.call_api(params, req, runtime)
        )

    async def flight_ota_item_detail_with_options_async(
        self,
        request: btrip_open_20220520_models.FlightOtaItemDetailRequest,
        headers: btrip_open_20220520_models.FlightOtaItemDetailHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightOtaItemDetailResponse:
        """
        @summary 查询退改规则行李额
        
        @param request: FlightOtaItemDetailRequest
        @param headers: FlightOtaItemDetailHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightOtaItemDetailResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.isv_name):
            query['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.ota_item_id):
            query['ota_item_id'] = request.ota_item_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='FlightOtaItemDetail',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v1/flight/action/ota-item-detail',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightOtaItemDetailResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def flight_ota_item_detail(
        self,
        request: btrip_open_20220520_models.FlightOtaItemDetailRequest,
    ) -> btrip_open_20220520_models.FlightOtaItemDetailResponse:
        """
        @summary 查询退改规则行李额
        
        @param request: FlightOtaItemDetailRequest
        @return: FlightOtaItemDetailResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightOtaItemDetailHeaders()
        return self.flight_ota_item_detail_with_options(request, headers, runtime)

    async def flight_ota_item_detail_async(
        self,
        request: btrip_open_20220520_models.FlightOtaItemDetailRequest,
    ) -> btrip_open_20220520_models.FlightOtaItemDetailResponse:
        """
        @summary 查询退改规则行李额
        
        @param request: FlightOtaItemDetailRequest
        @return: FlightOtaItemDetailResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightOtaItemDetailHeaders()
        return await self.flight_ota_item_detail_with_options_async(request, headers, runtime)

    def flight_ota_search_with_options(
        self,
        request: btrip_open_20220520_models.FlightOtaSearchRequest,
        headers: btrip_open_20220520_models.FlightOtaSearchHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightOtaSearchResponse:
        """
        @summary 航班最低价搜索
        
        @param request: FlightOtaSearchRequest
        @param headers: FlightOtaSearchHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightOtaSearchResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.airline_code):
            query['airline_code'] = request.airline_code
        if not UtilClient.is_unset(request.arr_city_code):
            query['arr_city_code'] = request.arr_city_code
        if not UtilClient.is_unset(request.cabin_class):
            query['cabin_class'] = request.cabin_class
        if not UtilClient.is_unset(request.carrier_flight_no):
            query['carrier_flight_no'] = request.carrier_flight_no
        if not UtilClient.is_unset(request.dep_city_code):
            query['dep_city_code'] = request.dep_city_code
        if not UtilClient.is_unset(request.dep_date):
            query['dep_date'] = request.dep_date
        if not UtilClient.is_unset(request.flight_no):
            query['flight_no'] = request.flight_no
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='FlightOtaSearch',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v1/flight/action/ota-search',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightOtaSearchResponse(),
            self.call_api(params, req, runtime)
        )

    async def flight_ota_search_with_options_async(
        self,
        request: btrip_open_20220520_models.FlightOtaSearchRequest,
        headers: btrip_open_20220520_models.FlightOtaSearchHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightOtaSearchResponse:
        """
        @summary 航班最低价搜索
        
        @param request: FlightOtaSearchRequest
        @param headers: FlightOtaSearchHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightOtaSearchResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.airline_code):
            query['airline_code'] = request.airline_code
        if not UtilClient.is_unset(request.arr_city_code):
            query['arr_city_code'] = request.arr_city_code
        if not UtilClient.is_unset(request.cabin_class):
            query['cabin_class'] = request.cabin_class
        if not UtilClient.is_unset(request.carrier_flight_no):
            query['carrier_flight_no'] = request.carrier_flight_no
        if not UtilClient.is_unset(request.dep_city_code):
            query['dep_city_code'] = request.dep_city_code
        if not UtilClient.is_unset(request.dep_date):
            query['dep_date'] = request.dep_date
        if not UtilClient.is_unset(request.flight_no):
            query['flight_no'] = request.flight_no
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='FlightOtaSearch',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v1/flight/action/ota-search',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightOtaSearchResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def flight_ota_search(
        self,
        request: btrip_open_20220520_models.FlightOtaSearchRequest,
    ) -> btrip_open_20220520_models.FlightOtaSearchResponse:
        """
        @summary 航班最低价搜索
        
        @param request: FlightOtaSearchRequest
        @return: FlightOtaSearchResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightOtaSearchHeaders()
        return self.flight_ota_search_with_options(request, headers, runtime)

    async def flight_ota_search_async(
        self,
        request: btrip_open_20220520_models.FlightOtaSearchRequest,
    ) -> btrip_open_20220520_models.FlightOtaSearchResponse:
        """
        @summary 航班最低价搜索
        
        @param request: FlightOtaSearchRequest
        @return: FlightOtaSearchResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightOtaSearchHeaders()
        return await self.flight_ota_search_with_options_async(request, headers, runtime)

    def flight_ota_search_v2with_options(
        self,
        tmp_req: btrip_open_20220520_models.FlightOtaSearchV2Request,
        headers: btrip_open_20220520_models.FlightOtaSearchV2Headers,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightOtaSearchV2Response:
        """
        @summary 单航班报价搜索
        
        @param tmp_req: FlightOtaSearchV2Request
        @param headers: FlightOtaSearchV2Headers
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightOtaSearchV2Response
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.FlightOtaSearchV2ShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.cabin_type_list):
            request.cabin_type_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.cabin_type_list, 'cabin_type_list', 'json')
        if not UtilClient.is_unset(tmp_req.search_journeys):
            request.search_journeys_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.search_journeys, 'search_journeys', 'json')
        query = {}
        if not UtilClient.is_unset(request.cabin_type_list_shrink):
            query['cabin_type_list'] = request.cabin_type_list_shrink
        if not UtilClient.is_unset(request.direct_only):
            query['direct_only'] = request.direct_only
        if not UtilClient.is_unset(request.isv_name):
            query['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.need_share_flight):
            query['need_share_flight'] = request.need_share_flight
        if not UtilClient.is_unset(request.search_journeys_shrink):
            query['search_journeys'] = request.search_journeys_shrink
        if not UtilClient.is_unset(request.search_mode):
            query['search_mode'] = request.search_mode
        if not UtilClient.is_unset(request.trip_type):
            query['trip_type'] = request.trip_type
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='FlightOtaSearchV2',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v2/flight/action/ota-search',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightOtaSearchV2Response(),
            self.call_api(params, req, runtime)
        )

    async def flight_ota_search_v2with_options_async(
        self,
        tmp_req: btrip_open_20220520_models.FlightOtaSearchV2Request,
        headers: btrip_open_20220520_models.FlightOtaSearchV2Headers,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightOtaSearchV2Response:
        """
        @summary 单航班报价搜索
        
        @param tmp_req: FlightOtaSearchV2Request
        @param headers: FlightOtaSearchV2Headers
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightOtaSearchV2Response
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.FlightOtaSearchV2ShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.cabin_type_list):
            request.cabin_type_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.cabin_type_list, 'cabin_type_list', 'json')
        if not UtilClient.is_unset(tmp_req.search_journeys):
            request.search_journeys_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.search_journeys, 'search_journeys', 'json')
        query = {}
        if not UtilClient.is_unset(request.cabin_type_list_shrink):
            query['cabin_type_list'] = request.cabin_type_list_shrink
        if not UtilClient.is_unset(request.direct_only):
            query['direct_only'] = request.direct_only
        if not UtilClient.is_unset(request.isv_name):
            query['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.need_share_flight):
            query['need_share_flight'] = request.need_share_flight
        if not UtilClient.is_unset(request.search_journeys_shrink):
            query['search_journeys'] = request.search_journeys_shrink
        if not UtilClient.is_unset(request.search_mode):
            query['search_mode'] = request.search_mode
        if not UtilClient.is_unset(request.trip_type):
            query['trip_type'] = request.trip_type
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='FlightOtaSearchV2',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v2/flight/action/ota-search',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightOtaSearchV2Response(),
            await self.call_api_async(params, req, runtime)
        )

    def flight_ota_search_v2(
        self,
        request: btrip_open_20220520_models.FlightOtaSearchV2Request,
    ) -> btrip_open_20220520_models.FlightOtaSearchV2Response:
        """
        @summary 单航班报价搜索
        
        @param request: FlightOtaSearchV2Request
        @return: FlightOtaSearchV2Response
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightOtaSearchV2Headers()
        return self.flight_ota_search_v2with_options(request, headers, runtime)

    async def flight_ota_search_v2_async(
        self,
        request: btrip_open_20220520_models.FlightOtaSearchV2Request,
    ) -> btrip_open_20220520_models.FlightOtaSearchV2Response:
        """
        @summary 单航班报价搜索
        
        @param request: FlightOtaSearchV2Request
        @return: FlightOtaSearchV2Response
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightOtaSearchV2Headers()
        return await self.flight_ota_search_v2with_options_async(request, headers, runtime)

    def flight_pay_order_with_options(
        self,
        tmp_req: btrip_open_20220520_models.FlightPayOrderRequest,
        headers: btrip_open_20220520_models.FlightPayOrderHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightPayOrderResponse:
        """
        @summary 航班订单支付
        
        @param tmp_req: FlightPayOrderRequest
        @param headers: FlightPayOrderHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightPayOrderResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.FlightPayOrderShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.extra):
            request.extra_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.extra, 'extra', 'json')
        body = {}
        if not UtilClient.is_unset(request.corp_pay_price):
            body['corp_pay_price'] = request.corp_pay_price
        if not UtilClient.is_unset(request.dis_order_id):
            body['dis_order_id'] = request.dis_order_id
        if not UtilClient.is_unset(request.extra_shrink):
            body['extra'] = request.extra_shrink
        if not UtilClient.is_unset(request.personal_pay_price):
            body['personal_pay_price'] = request.personal_pay_price
        if not UtilClient.is_unset(request.total_pay_price):
            body['total_pay_price'] = request.total_pay_price
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='FlightPayOrder',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v1/order/action/pay',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightPayOrderResponse(),
            self.call_api(params, req, runtime)
        )

    async def flight_pay_order_with_options_async(
        self,
        tmp_req: btrip_open_20220520_models.FlightPayOrderRequest,
        headers: btrip_open_20220520_models.FlightPayOrderHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightPayOrderResponse:
        """
        @summary 航班订单支付
        
        @param tmp_req: FlightPayOrderRequest
        @param headers: FlightPayOrderHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightPayOrderResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.FlightPayOrderShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.extra):
            request.extra_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.extra, 'extra', 'json')
        body = {}
        if not UtilClient.is_unset(request.corp_pay_price):
            body['corp_pay_price'] = request.corp_pay_price
        if not UtilClient.is_unset(request.dis_order_id):
            body['dis_order_id'] = request.dis_order_id
        if not UtilClient.is_unset(request.extra_shrink):
            body['extra'] = request.extra_shrink
        if not UtilClient.is_unset(request.personal_pay_price):
            body['personal_pay_price'] = request.personal_pay_price
        if not UtilClient.is_unset(request.total_pay_price):
            body['total_pay_price'] = request.total_pay_price
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='FlightPayOrder',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v1/order/action/pay',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightPayOrderResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def flight_pay_order(
        self,
        request: btrip_open_20220520_models.FlightPayOrderRequest,
    ) -> btrip_open_20220520_models.FlightPayOrderResponse:
        """
        @summary 航班订单支付
        
        @param request: FlightPayOrderRequest
        @return: FlightPayOrderResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightPayOrderHeaders()
        return self.flight_pay_order_with_options(request, headers, runtime)

    async def flight_pay_order_async(
        self,
        request: btrip_open_20220520_models.FlightPayOrderRequest,
    ) -> btrip_open_20220520_models.FlightPayOrderResponse:
        """
        @summary 航班订单支付
        
        @param request: FlightPayOrderRequest
        @return: FlightPayOrderResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightPayOrderHeaders()
        return await self.flight_pay_order_with_options_async(request, headers, runtime)

    def flight_pay_order_v2with_options(
        self,
        request: btrip_open_20220520_models.FlightPayOrderV2Request,
        headers: btrip_open_20220520_models.FlightPayOrderV2Headers,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightPayOrderV2Response:
        """
        @summary 机票订单支付
        
        @param request: FlightPayOrderV2Request
        @param headers: FlightPayOrderV2Headers
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightPayOrderV2Response
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.isv_name):
            body['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.order_id):
            body['order_id'] = request.order_id
        if not UtilClient.is_unset(request.out_order_id):
            body['out_order_id'] = request.out_order_id
        if not UtilClient.is_unset(request.total_price):
            body['total_price'] = request.total_price
        if not UtilClient.is_unset(request.total_service_fee_price):
            body['total_service_fee_price'] = request.total_service_fee_price
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='FlightPayOrderV2',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v2/order/action/pay',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightPayOrderV2Response(),
            self.call_api(params, req, runtime)
        )

    async def flight_pay_order_v2with_options_async(
        self,
        request: btrip_open_20220520_models.FlightPayOrderV2Request,
        headers: btrip_open_20220520_models.FlightPayOrderV2Headers,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightPayOrderV2Response:
        """
        @summary 机票订单支付
        
        @param request: FlightPayOrderV2Request
        @param headers: FlightPayOrderV2Headers
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightPayOrderV2Response
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.isv_name):
            body['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.order_id):
            body['order_id'] = request.order_id
        if not UtilClient.is_unset(request.out_order_id):
            body['out_order_id'] = request.out_order_id
        if not UtilClient.is_unset(request.total_price):
            body['total_price'] = request.total_price
        if not UtilClient.is_unset(request.total_service_fee_price):
            body['total_service_fee_price'] = request.total_service_fee_price
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='FlightPayOrderV2',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v2/order/action/pay',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightPayOrderV2Response(),
            await self.call_api_async(params, req, runtime)
        )

    def flight_pay_order_v2(
        self,
        request: btrip_open_20220520_models.FlightPayOrderV2Request,
    ) -> btrip_open_20220520_models.FlightPayOrderV2Response:
        """
        @summary 机票订单支付
        
        @param request: FlightPayOrderV2Request
        @return: FlightPayOrderV2Response
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightPayOrderV2Headers()
        return self.flight_pay_order_v2with_options(request, headers, runtime)

    async def flight_pay_order_v2_async(
        self,
        request: btrip_open_20220520_models.FlightPayOrderV2Request,
    ) -> btrip_open_20220520_models.FlightPayOrderV2Response:
        """
        @summary 机票订单支付
        
        @param request: FlightPayOrderV2Request
        @return: FlightPayOrderV2Response
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightPayOrderV2Headers()
        return await self.flight_pay_order_v2with_options_async(request, headers, runtime)

    def flight_refund_apply_with_options(
        self,
        tmp_req: btrip_open_20220520_models.FlightRefundApplyRequest,
        headers: btrip_open_20220520_models.FlightRefundApplyHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightRefundApplyResponse:
        """
        @summary 航班退票申请
        
        @param tmp_req: FlightRefundApplyRequest
        @param headers: FlightRefundApplyHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightRefundApplyResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.FlightRefundApplyShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.extra):
            request.extra_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.extra, 'extra', 'json')
        if not UtilClient.is_unset(tmp_req.passenger_segment_info_list):
            request.passenger_segment_info_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.passenger_segment_info_list, 'passenger_segment_info_list', 'json')
        if not UtilClient.is_unset(tmp_req.refund_voucher_info):
            request.refund_voucher_info_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.refund_voucher_info, 'refund_voucher_info', 'json')
        body = {}
        if not UtilClient.is_unset(request.corp_refund_price):
            body['corp_refund_price'] = request.corp_refund_price
        if not UtilClient.is_unset(request.dis_order_id):
            body['dis_order_id'] = request.dis_order_id
        if not UtilClient.is_unset(request.dis_sub_order_id):
            body['dis_sub_order_id'] = request.dis_sub_order_id
        if not UtilClient.is_unset(request.display_refund_money):
            body['display_refund_money'] = request.display_refund_money
        if not UtilClient.is_unset(request.extra_shrink):
            body['extra'] = request.extra_shrink
        if not UtilClient.is_unset(request.is_voluntary):
            body['is_voluntary'] = request.is_voluntary
        if not UtilClient.is_unset(request.item_unit_ids):
            body['item_unit_ids'] = request.item_unit_ids
        if not UtilClient.is_unset(request.passenger_segment_info_list_shrink):
            body['passenger_segment_info_list'] = request.passenger_segment_info_list_shrink
        if not UtilClient.is_unset(request.personal_refund_price):
            body['personal_refund_price'] = request.personal_refund_price
        if not UtilClient.is_unset(request.reason_detail):
            body['reason_detail'] = request.reason_detail
        if not UtilClient.is_unset(request.reason_type):
            body['reason_type'] = request.reason_type
        if not UtilClient.is_unset(request.refund_voucher_info_shrink):
            body['refund_voucher_info'] = request.refund_voucher_info_shrink
        if not UtilClient.is_unset(request.session_id):
            body['session_id'] = request.session_id
        if not UtilClient.is_unset(request.total_refund_price):
            body['total_refund_price'] = request.total_refund_price
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='FlightRefundApply',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v1/refund/action/apply',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightRefundApplyResponse(),
            self.call_api(params, req, runtime)
        )

    async def flight_refund_apply_with_options_async(
        self,
        tmp_req: btrip_open_20220520_models.FlightRefundApplyRequest,
        headers: btrip_open_20220520_models.FlightRefundApplyHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightRefundApplyResponse:
        """
        @summary 航班退票申请
        
        @param tmp_req: FlightRefundApplyRequest
        @param headers: FlightRefundApplyHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightRefundApplyResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.FlightRefundApplyShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.extra):
            request.extra_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.extra, 'extra', 'json')
        if not UtilClient.is_unset(tmp_req.passenger_segment_info_list):
            request.passenger_segment_info_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.passenger_segment_info_list, 'passenger_segment_info_list', 'json')
        if not UtilClient.is_unset(tmp_req.refund_voucher_info):
            request.refund_voucher_info_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.refund_voucher_info, 'refund_voucher_info', 'json')
        body = {}
        if not UtilClient.is_unset(request.corp_refund_price):
            body['corp_refund_price'] = request.corp_refund_price
        if not UtilClient.is_unset(request.dis_order_id):
            body['dis_order_id'] = request.dis_order_id
        if not UtilClient.is_unset(request.dis_sub_order_id):
            body['dis_sub_order_id'] = request.dis_sub_order_id
        if not UtilClient.is_unset(request.display_refund_money):
            body['display_refund_money'] = request.display_refund_money
        if not UtilClient.is_unset(request.extra_shrink):
            body['extra'] = request.extra_shrink
        if not UtilClient.is_unset(request.is_voluntary):
            body['is_voluntary'] = request.is_voluntary
        if not UtilClient.is_unset(request.item_unit_ids):
            body['item_unit_ids'] = request.item_unit_ids
        if not UtilClient.is_unset(request.passenger_segment_info_list_shrink):
            body['passenger_segment_info_list'] = request.passenger_segment_info_list_shrink
        if not UtilClient.is_unset(request.personal_refund_price):
            body['personal_refund_price'] = request.personal_refund_price
        if not UtilClient.is_unset(request.reason_detail):
            body['reason_detail'] = request.reason_detail
        if not UtilClient.is_unset(request.reason_type):
            body['reason_type'] = request.reason_type
        if not UtilClient.is_unset(request.refund_voucher_info_shrink):
            body['refund_voucher_info'] = request.refund_voucher_info_shrink
        if not UtilClient.is_unset(request.session_id):
            body['session_id'] = request.session_id
        if not UtilClient.is_unset(request.total_refund_price):
            body['total_refund_price'] = request.total_refund_price
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='FlightRefundApply',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v1/refund/action/apply',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightRefundApplyResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def flight_refund_apply(
        self,
        request: btrip_open_20220520_models.FlightRefundApplyRequest,
    ) -> btrip_open_20220520_models.FlightRefundApplyResponse:
        """
        @summary 航班退票申请
        
        @param request: FlightRefundApplyRequest
        @return: FlightRefundApplyResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightRefundApplyHeaders()
        return self.flight_refund_apply_with_options(request, headers, runtime)

    async def flight_refund_apply_async(
        self,
        request: btrip_open_20220520_models.FlightRefundApplyRequest,
    ) -> btrip_open_20220520_models.FlightRefundApplyResponse:
        """
        @summary 航班退票申请
        
        @param request: FlightRefundApplyRequest
        @return: FlightRefundApplyResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightRefundApplyHeaders()
        return await self.flight_refund_apply_with_options_async(request, headers, runtime)

    def flight_refund_apply_v2with_options(
        self,
        tmp_req: btrip_open_20220520_models.FlightRefundApplyV2Request,
        headers: btrip_open_20220520_models.FlightRefundApplyV2Headers,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightRefundApplyV2Response:
        """
        @summary 机票退票申请
        
        @param tmp_req: FlightRefundApplyV2Request
        @param headers: FlightRefundApplyV2Headers
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightRefundApplyV2Response
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.FlightRefundApplyV2ShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.passenger_segment_relations):
            request.passenger_segment_relations_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.passenger_segment_relations, 'passenger_segment_relations', 'json')
        if not UtilClient.is_unset(tmp_req.ticket_nos):
            request.ticket_nos_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.ticket_nos, 'ticket_nos', 'json')
        body = {}
        if not UtilClient.is_unset(request.isv_name):
            body['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.order_id):
            body['order_id'] = request.order_id
        if not UtilClient.is_unset(request.out_order_id):
            body['out_order_id'] = request.out_order_id
        if not UtilClient.is_unset(request.out_sub_order_id):
            body['out_sub_order_id'] = request.out_sub_order_id
        if not UtilClient.is_unset(request.passenger_segment_relations_shrink):
            body['passenger_segment_relations'] = request.passenger_segment_relations_shrink
        if not UtilClient.is_unset(request.pre_cal_type):
            body['pre_cal_type'] = request.pre_cal_type
        if not UtilClient.is_unset(request.refund_reason):
            body['refund_reason'] = request.refund_reason
        if not UtilClient.is_unset(request.refund_reason_type):
            body['refund_reason_type'] = request.refund_reason_type
        if not UtilClient.is_unset(request.ticket_nos_shrink):
            body['ticket_nos'] = request.ticket_nos_shrink
        if not UtilClient.is_unset(request.total_refund_price):
            body['total_refund_price'] = request.total_refund_price
        if not UtilClient.is_unset(request.upload_pict_urls):
            body['upload_pict_urls'] = request.upload_pict_urls
        if not UtilClient.is_unset(request.voluntary):
            body['voluntary'] = request.voluntary
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='FlightRefundApplyV2',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v2/refund/action/apply',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightRefundApplyV2Response(),
            self.call_api(params, req, runtime)
        )

    async def flight_refund_apply_v2with_options_async(
        self,
        tmp_req: btrip_open_20220520_models.FlightRefundApplyV2Request,
        headers: btrip_open_20220520_models.FlightRefundApplyV2Headers,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightRefundApplyV2Response:
        """
        @summary 机票退票申请
        
        @param tmp_req: FlightRefundApplyV2Request
        @param headers: FlightRefundApplyV2Headers
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightRefundApplyV2Response
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.FlightRefundApplyV2ShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.passenger_segment_relations):
            request.passenger_segment_relations_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.passenger_segment_relations, 'passenger_segment_relations', 'json')
        if not UtilClient.is_unset(tmp_req.ticket_nos):
            request.ticket_nos_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.ticket_nos, 'ticket_nos', 'json')
        body = {}
        if not UtilClient.is_unset(request.isv_name):
            body['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.order_id):
            body['order_id'] = request.order_id
        if not UtilClient.is_unset(request.out_order_id):
            body['out_order_id'] = request.out_order_id
        if not UtilClient.is_unset(request.out_sub_order_id):
            body['out_sub_order_id'] = request.out_sub_order_id
        if not UtilClient.is_unset(request.passenger_segment_relations_shrink):
            body['passenger_segment_relations'] = request.passenger_segment_relations_shrink
        if not UtilClient.is_unset(request.pre_cal_type):
            body['pre_cal_type'] = request.pre_cal_type
        if not UtilClient.is_unset(request.refund_reason):
            body['refund_reason'] = request.refund_reason
        if not UtilClient.is_unset(request.refund_reason_type):
            body['refund_reason_type'] = request.refund_reason_type
        if not UtilClient.is_unset(request.ticket_nos_shrink):
            body['ticket_nos'] = request.ticket_nos_shrink
        if not UtilClient.is_unset(request.total_refund_price):
            body['total_refund_price'] = request.total_refund_price
        if not UtilClient.is_unset(request.upload_pict_urls):
            body['upload_pict_urls'] = request.upload_pict_urls
        if not UtilClient.is_unset(request.voluntary):
            body['voluntary'] = request.voluntary
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='FlightRefundApplyV2',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v2/refund/action/apply',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightRefundApplyV2Response(),
            await self.call_api_async(params, req, runtime)
        )

    def flight_refund_apply_v2(
        self,
        request: btrip_open_20220520_models.FlightRefundApplyV2Request,
    ) -> btrip_open_20220520_models.FlightRefundApplyV2Response:
        """
        @summary 机票退票申请
        
        @param request: FlightRefundApplyV2Request
        @return: FlightRefundApplyV2Response
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightRefundApplyV2Headers()
        return self.flight_refund_apply_v2with_options(request, headers, runtime)

    async def flight_refund_apply_v2_async(
        self,
        request: btrip_open_20220520_models.FlightRefundApplyV2Request,
    ) -> btrip_open_20220520_models.FlightRefundApplyV2Response:
        """
        @summary 机票退票申请
        
        @param request: FlightRefundApplyV2Request
        @return: FlightRefundApplyV2Response
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightRefundApplyV2Headers()
        return await self.flight_refund_apply_v2with_options_async(request, headers, runtime)

    def flight_refund_detail_with_options(
        self,
        request: btrip_open_20220520_models.FlightRefundDetailRequest,
        headers: btrip_open_20220520_models.FlightRefundDetailHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightRefundDetailResponse:
        """
        @summary 航班退票详情
        
        @param request: FlightRefundDetailRequest
        @param headers: FlightRefundDetailHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightRefundDetailResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.dis_order_id):
            query['dis_order_id'] = request.dis_order_id
        if not UtilClient.is_unset(request.dis_sub_order_id):
            query['dis_sub_order_id'] = request.dis_sub_order_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='FlightRefundDetail',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v1/refund/action/detail',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightRefundDetailResponse(),
            self.call_api(params, req, runtime)
        )

    async def flight_refund_detail_with_options_async(
        self,
        request: btrip_open_20220520_models.FlightRefundDetailRequest,
        headers: btrip_open_20220520_models.FlightRefundDetailHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightRefundDetailResponse:
        """
        @summary 航班退票详情
        
        @param request: FlightRefundDetailRequest
        @param headers: FlightRefundDetailHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightRefundDetailResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.dis_order_id):
            query['dis_order_id'] = request.dis_order_id
        if not UtilClient.is_unset(request.dis_sub_order_id):
            query['dis_sub_order_id'] = request.dis_sub_order_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='FlightRefundDetail',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v1/refund/action/detail',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightRefundDetailResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def flight_refund_detail(
        self,
        request: btrip_open_20220520_models.FlightRefundDetailRequest,
    ) -> btrip_open_20220520_models.FlightRefundDetailResponse:
        """
        @summary 航班退票详情
        
        @param request: FlightRefundDetailRequest
        @return: FlightRefundDetailResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightRefundDetailHeaders()
        return self.flight_refund_detail_with_options(request, headers, runtime)

    async def flight_refund_detail_async(
        self,
        request: btrip_open_20220520_models.FlightRefundDetailRequest,
    ) -> btrip_open_20220520_models.FlightRefundDetailResponse:
        """
        @summary 航班退票详情
        
        @param request: FlightRefundDetailRequest
        @return: FlightRefundDetailResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightRefundDetailHeaders()
        return await self.flight_refund_detail_with_options_async(request, headers, runtime)

    def flight_refund_detail_v2with_options(
        self,
        request: btrip_open_20220520_models.FlightRefundDetailV2Request,
        headers: btrip_open_20220520_models.FlightRefundDetailV2Headers,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightRefundDetailV2Response:
        """
        @summary 机票退票详情
        
        @param request: FlightRefundDetailV2Request
        @param headers: FlightRefundDetailV2Headers
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightRefundDetailV2Response
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.isv_name):
            query['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.order_id):
            query['order_id'] = request.order_id
        if not UtilClient.is_unset(request.refund_apply_id):
            query['refund_apply_id'] = request.refund_apply_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='FlightRefundDetailV2',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v2/refund/action/detail',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightRefundDetailV2Response(),
            self.call_api(params, req, runtime)
        )

    async def flight_refund_detail_v2with_options_async(
        self,
        request: btrip_open_20220520_models.FlightRefundDetailV2Request,
        headers: btrip_open_20220520_models.FlightRefundDetailV2Headers,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightRefundDetailV2Response:
        """
        @summary 机票退票详情
        
        @param request: FlightRefundDetailV2Request
        @param headers: FlightRefundDetailV2Headers
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightRefundDetailV2Response
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.isv_name):
            query['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.order_id):
            query['order_id'] = request.order_id
        if not UtilClient.is_unset(request.refund_apply_id):
            query['refund_apply_id'] = request.refund_apply_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='FlightRefundDetailV2',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v2/refund/action/detail',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightRefundDetailV2Response(),
            await self.call_api_async(params, req, runtime)
        )

    def flight_refund_detail_v2(
        self,
        request: btrip_open_20220520_models.FlightRefundDetailV2Request,
    ) -> btrip_open_20220520_models.FlightRefundDetailV2Response:
        """
        @summary 机票退票详情
        
        @param request: FlightRefundDetailV2Request
        @return: FlightRefundDetailV2Response
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightRefundDetailV2Headers()
        return self.flight_refund_detail_v2with_options(request, headers, runtime)

    async def flight_refund_detail_v2_async(
        self,
        request: btrip_open_20220520_models.FlightRefundDetailV2Request,
    ) -> btrip_open_20220520_models.FlightRefundDetailV2Response:
        """
        @summary 机票退票详情
        
        @param request: FlightRefundDetailV2Request
        @return: FlightRefundDetailV2Response
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightRefundDetailV2Headers()
        return await self.flight_refund_detail_v2with_options_async(request, headers, runtime)

    def flight_refund_pre_cal_with_options(
        self,
        tmp_req: btrip_open_20220520_models.FlightRefundPreCalRequest,
        headers: btrip_open_20220520_models.FlightRefundPreCalHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightRefundPreCalResponse:
        """
        @summary 机票退票预计算
        
        @param tmp_req: FlightRefundPreCalRequest
        @param headers: FlightRefundPreCalHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightRefundPreCalResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.FlightRefundPreCalShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.passenger_segment_info_list):
            request.passenger_segment_info_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.passenger_segment_info_list, 'passenger_segment_info_list', 'json')
        query = {}
        if not UtilClient.is_unset(request.dis_order_id):
            query['dis_order_id'] = request.dis_order_id
        if not UtilClient.is_unset(request.is_voluntary):
            query['is_voluntary'] = request.is_voluntary
        if not UtilClient.is_unset(request.passenger_segment_info_list_shrink):
            query['passenger_segment_info_list'] = request.passenger_segment_info_list_shrink
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='FlightRefundPreCal',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v1/refund/action/pre-cal',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightRefundPreCalResponse(),
            self.call_api(params, req, runtime)
        )

    async def flight_refund_pre_cal_with_options_async(
        self,
        tmp_req: btrip_open_20220520_models.FlightRefundPreCalRequest,
        headers: btrip_open_20220520_models.FlightRefundPreCalHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightRefundPreCalResponse:
        """
        @summary 机票退票预计算
        
        @param tmp_req: FlightRefundPreCalRequest
        @param headers: FlightRefundPreCalHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightRefundPreCalResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.FlightRefundPreCalShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.passenger_segment_info_list):
            request.passenger_segment_info_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.passenger_segment_info_list, 'passenger_segment_info_list', 'json')
        query = {}
        if not UtilClient.is_unset(request.dis_order_id):
            query['dis_order_id'] = request.dis_order_id
        if not UtilClient.is_unset(request.is_voluntary):
            query['is_voluntary'] = request.is_voluntary
        if not UtilClient.is_unset(request.passenger_segment_info_list_shrink):
            query['passenger_segment_info_list'] = request.passenger_segment_info_list_shrink
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='FlightRefundPreCal',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v1/refund/action/pre-cal',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightRefundPreCalResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def flight_refund_pre_cal(
        self,
        request: btrip_open_20220520_models.FlightRefundPreCalRequest,
    ) -> btrip_open_20220520_models.FlightRefundPreCalResponse:
        """
        @summary 机票退票预计算
        
        @param request: FlightRefundPreCalRequest
        @return: FlightRefundPreCalResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightRefundPreCalHeaders()
        return self.flight_refund_pre_cal_with_options(request, headers, runtime)

    async def flight_refund_pre_cal_async(
        self,
        request: btrip_open_20220520_models.FlightRefundPreCalRequest,
    ) -> btrip_open_20220520_models.FlightRefundPreCalResponse:
        """
        @summary 机票退票预计算
        
        @param request: FlightRefundPreCalRequest
        @return: FlightRefundPreCalResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightRefundPreCalHeaders()
        return await self.flight_refund_pre_cal_with_options_async(request, headers, runtime)

    def flight_refund_pre_cal_v2with_options(
        self,
        tmp_req: btrip_open_20220520_models.FlightRefundPreCalV2Request,
        headers: btrip_open_20220520_models.FlightRefundPreCalV2Headers,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightRefundPreCalV2Response:
        """
        @summary 机票退票费用预计算
        
        @param tmp_req: FlightRefundPreCalV2Request
        @param headers: FlightRefundPreCalV2Headers
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightRefundPreCalV2Response
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.FlightRefundPreCalV2ShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.passenger_segment_relations):
            request.passenger_segment_relations_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.passenger_segment_relations, 'passenger_segment_relations', 'json')
        if not UtilClient.is_unset(tmp_req.ticket_nos):
            request.ticket_nos_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.ticket_nos, 'ticket_nos', 'json')
        query = {}
        if not UtilClient.is_unset(request.isv_name):
            query['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.order_id):
            query['order_id'] = request.order_id
        if not UtilClient.is_unset(request.out_order_id):
            query['out_order_id'] = request.out_order_id
        if not UtilClient.is_unset(request.passenger_segment_relations_shrink):
            query['passenger_segment_relations'] = request.passenger_segment_relations_shrink
        if not UtilClient.is_unset(request.pre_cal_type):
            query['pre_cal_type'] = request.pre_cal_type
        if not UtilClient.is_unset(request.ticket_nos_shrink):
            query['ticket_nos'] = request.ticket_nos_shrink
        if not UtilClient.is_unset(request.voluntary):
            query['voluntary'] = request.voluntary
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='FlightRefundPreCalV2',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v2/refund/action/pre-cal',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightRefundPreCalV2Response(),
            self.call_api(params, req, runtime)
        )

    async def flight_refund_pre_cal_v2with_options_async(
        self,
        tmp_req: btrip_open_20220520_models.FlightRefundPreCalV2Request,
        headers: btrip_open_20220520_models.FlightRefundPreCalV2Headers,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightRefundPreCalV2Response:
        """
        @summary 机票退票费用预计算
        
        @param tmp_req: FlightRefundPreCalV2Request
        @param headers: FlightRefundPreCalV2Headers
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightRefundPreCalV2Response
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.FlightRefundPreCalV2ShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.passenger_segment_relations):
            request.passenger_segment_relations_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.passenger_segment_relations, 'passenger_segment_relations', 'json')
        if not UtilClient.is_unset(tmp_req.ticket_nos):
            request.ticket_nos_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.ticket_nos, 'ticket_nos', 'json')
        query = {}
        if not UtilClient.is_unset(request.isv_name):
            query['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.order_id):
            query['order_id'] = request.order_id
        if not UtilClient.is_unset(request.out_order_id):
            query['out_order_id'] = request.out_order_id
        if not UtilClient.is_unset(request.passenger_segment_relations_shrink):
            query['passenger_segment_relations'] = request.passenger_segment_relations_shrink
        if not UtilClient.is_unset(request.pre_cal_type):
            query['pre_cal_type'] = request.pre_cal_type
        if not UtilClient.is_unset(request.ticket_nos_shrink):
            query['ticket_nos'] = request.ticket_nos_shrink
        if not UtilClient.is_unset(request.voluntary):
            query['voluntary'] = request.voluntary
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='FlightRefundPreCalV2',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v2/refund/action/pre-cal',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightRefundPreCalV2Response(),
            await self.call_api_async(params, req, runtime)
        )

    def flight_refund_pre_cal_v2(
        self,
        request: btrip_open_20220520_models.FlightRefundPreCalV2Request,
    ) -> btrip_open_20220520_models.FlightRefundPreCalV2Response:
        """
        @summary 机票退票费用预计算
        
        @param request: FlightRefundPreCalV2Request
        @return: FlightRefundPreCalV2Response
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightRefundPreCalV2Headers()
        return self.flight_refund_pre_cal_v2with_options(request, headers, runtime)

    async def flight_refund_pre_cal_v2_async(
        self,
        request: btrip_open_20220520_models.FlightRefundPreCalV2Request,
    ) -> btrip_open_20220520_models.FlightRefundPreCalV2Response:
        """
        @summary 机票退票费用预计算
        
        @param request: FlightRefundPreCalV2Request
        @return: FlightRefundPreCalV2Response
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightRefundPreCalV2Headers()
        return await self.flight_refund_pre_cal_v2with_options_async(request, headers, runtime)

    def flight_search_list_with_options(
        self,
        request: btrip_open_20220520_models.FlightSearchListRequest,
        headers: btrip_open_20220520_models.FlightSearchListHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightSearchListResponse:
        """
        @summary 航班列表搜索
        
        @param request: FlightSearchListRequest
        @param headers: FlightSearchListHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightSearchListResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.airline_code):
            query['airline_code'] = request.airline_code
        if not UtilClient.is_unset(request.arr_city_code):
            query['arr_city_code'] = request.arr_city_code
        if not UtilClient.is_unset(request.arr_city_name):
            query['arr_city_name'] = request.arr_city_name
        if not UtilClient.is_unset(request.arr_date):
            query['arr_date'] = request.arr_date
        if not UtilClient.is_unset(request.cabin_class):
            query['cabin_class'] = request.cabin_class
        if not UtilClient.is_unset(request.dep_city_code):
            query['dep_city_code'] = request.dep_city_code
        if not UtilClient.is_unset(request.dep_city_name):
            query['dep_city_name'] = request.dep_city_name
        if not UtilClient.is_unset(request.dep_date):
            query['dep_date'] = request.dep_date
        if not UtilClient.is_unset(request.flight_no):
            query['flight_no'] = request.flight_no
        if not UtilClient.is_unset(request.need_multi_class_price):
            query['need_multi_class_price'] = request.need_multi_class_price
        if not UtilClient.is_unset(request.transfer_city_code):
            query['transfer_city_code'] = request.transfer_city_code
        if not UtilClient.is_unset(request.transfer_flight_no):
            query['transfer_flight_no'] = request.transfer_flight_no
        if not UtilClient.is_unset(request.transfer_leave_date):
            query['transfer_leave_date'] = request.transfer_leave_date
        if not UtilClient.is_unset(request.trip_type):
            query['trip_type'] = request.trip_type
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='FlightSearchList',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/huge/dtb-flight/v1/flight/action/search-list',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightSearchListResponse(),
            self.call_api(params, req, runtime)
        )

    async def flight_search_list_with_options_async(
        self,
        request: btrip_open_20220520_models.FlightSearchListRequest,
        headers: btrip_open_20220520_models.FlightSearchListHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.FlightSearchListResponse:
        """
        @summary 航班列表搜索
        
        @param request: FlightSearchListRequest
        @param headers: FlightSearchListHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: FlightSearchListResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.airline_code):
            query['airline_code'] = request.airline_code
        if not UtilClient.is_unset(request.arr_city_code):
            query['arr_city_code'] = request.arr_city_code
        if not UtilClient.is_unset(request.arr_city_name):
            query['arr_city_name'] = request.arr_city_name
        if not UtilClient.is_unset(request.arr_date):
            query['arr_date'] = request.arr_date
        if not UtilClient.is_unset(request.cabin_class):
            query['cabin_class'] = request.cabin_class
        if not UtilClient.is_unset(request.dep_city_code):
            query['dep_city_code'] = request.dep_city_code
        if not UtilClient.is_unset(request.dep_city_name):
            query['dep_city_name'] = request.dep_city_name
        if not UtilClient.is_unset(request.dep_date):
            query['dep_date'] = request.dep_date
        if not UtilClient.is_unset(request.flight_no):
            query['flight_no'] = request.flight_no
        if not UtilClient.is_unset(request.need_multi_class_price):
            query['need_multi_class_price'] = request.need_multi_class_price
        if not UtilClient.is_unset(request.transfer_city_code):
            query['transfer_city_code'] = request.transfer_city_code
        if not UtilClient.is_unset(request.transfer_flight_no):
            query['transfer_flight_no'] = request.transfer_flight_no
        if not UtilClient.is_unset(request.transfer_leave_date):
            query['transfer_leave_date'] = request.transfer_leave_date
        if not UtilClient.is_unset(request.trip_type):
            query['trip_type'] = request.trip_type
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='FlightSearchList',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/huge/dtb-flight/v1/flight/action/search-list',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.FlightSearchListResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def flight_search_list(
        self,
        request: btrip_open_20220520_models.FlightSearchListRequest,
    ) -> btrip_open_20220520_models.FlightSearchListResponse:
        """
        @summary 航班列表搜索
        
        @param request: FlightSearchListRequest
        @return: FlightSearchListResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightSearchListHeaders()
        return self.flight_search_list_with_options(request, headers, runtime)

    async def flight_search_list_async(
        self,
        request: btrip_open_20220520_models.FlightSearchListRequest,
    ) -> btrip_open_20220520_models.FlightSearchListResponse:
        """
        @summary 航班列表搜索
        
        @param request: FlightSearchListRequest
        @return: FlightSearchListResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.FlightSearchListHeaders()
        return await self.flight_search_list_with_options_async(request, headers, runtime)

    def group_corp_token_with_options(
        self,
        request: btrip_open_20220520_models.GroupCorpTokenRequest,
        headers: btrip_open_20220520_models.GroupCorpTokenHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.GroupCorpTokenResponse:
        """
        @summary 换取GroupCorpToken接口
        
        @param request: GroupCorpTokenRequest
        @param headers: GroupCorpTokenHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: GroupCorpTokenResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.app_secret):
            query['app_secret'] = request.app_secret
        if not UtilClient.is_unset(request.corp_id):
            query['corp_id'] = request.corp_id
        if not UtilClient.is_unset(request.sub_corp_id):
            query['sub_corp_id'] = request.sub_corp_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_access_token):
            real_headers['x-acs-btrip-access-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GroupCorpToken',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/btrip-open-auth/v1/group-corp-token/action/take',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.GroupCorpTokenResponse(),
            self.call_api(params, req, runtime)
        )

    async def group_corp_token_with_options_async(
        self,
        request: btrip_open_20220520_models.GroupCorpTokenRequest,
        headers: btrip_open_20220520_models.GroupCorpTokenHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.GroupCorpTokenResponse:
        """
        @summary 换取GroupCorpToken接口
        
        @param request: GroupCorpTokenRequest
        @param headers: GroupCorpTokenHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: GroupCorpTokenResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.app_secret):
            query['app_secret'] = request.app_secret
        if not UtilClient.is_unset(request.corp_id):
            query['corp_id'] = request.corp_id
        if not UtilClient.is_unset(request.sub_corp_id):
            query['sub_corp_id'] = request.sub_corp_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_access_token):
            real_headers['x-acs-btrip-access-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_access_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='GroupCorpToken',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/btrip-open-auth/v1/group-corp-token/action/take',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.GroupCorpTokenResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def group_corp_token(
        self,
        request: btrip_open_20220520_models.GroupCorpTokenRequest,
    ) -> btrip_open_20220520_models.GroupCorpTokenResponse:
        """
        @summary 换取GroupCorpToken接口
        
        @param request: GroupCorpTokenRequest
        @return: GroupCorpTokenResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.GroupCorpTokenHeaders()
        return self.group_corp_token_with_options(request, headers, runtime)

    async def group_corp_token_async(
        self,
        request: btrip_open_20220520_models.GroupCorpTokenRequest,
    ) -> btrip_open_20220520_models.GroupCorpTokenResponse:
        """
        @summary 换取GroupCorpToken接口
        
        @param request: GroupCorpTokenRequest
        @return: GroupCorpTokenResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.GroupCorpTokenHeaders()
        return await self.group_corp_token_with_options_async(request, headers, runtime)

    def group_depart_save_with_options(
        self,
        tmp_req: btrip_open_20220520_models.GroupDepartSaveRequest,
        headers: btrip_open_20220520_models.GroupDepartSaveHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.GroupDepartSaveResponse:
        """
        @summary 集团部门同步
        
        @param tmp_req: GroupDepartSaveRequest
        @param headers: GroupDepartSaveHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: GroupDepartSaveResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.GroupDepartSaveShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.sub_corp_id_list):
            request.sub_corp_id_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.sub_corp_id_list, 'sub_corp_id_list', 'json')
        body = {}
        if not UtilClient.is_unset(request.dept_name):
            body['dept_name'] = request.dept_name
        if not UtilClient.is_unset(request.manager_ids):
            body['manager_ids'] = request.manager_ids
        if not UtilClient.is_unset(request.outer_dept_id):
            body['outer_dept_id'] = request.outer_dept_id
        if not UtilClient.is_unset(request.outer_dept_pid):
            body['outer_dept_pid'] = request.outer_dept_pid
        if not UtilClient.is_unset(request.status):
            body['status'] = request.status
        if not UtilClient.is_unset(request.sub_corp_id_list_shrink):
            body['sub_corp_id_list'] = request.sub_corp_id_list_shrink
        if not UtilClient.is_unset(request.sync_group):
            body['sync_group'] = request.sync_group
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='GroupDepartSave',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/sub_corps/v1/departs',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.GroupDepartSaveResponse(),
            self.call_api(params, req, runtime)
        )

    async def group_depart_save_with_options_async(
        self,
        tmp_req: btrip_open_20220520_models.GroupDepartSaveRequest,
        headers: btrip_open_20220520_models.GroupDepartSaveHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.GroupDepartSaveResponse:
        """
        @summary 集团部门同步
        
        @param tmp_req: GroupDepartSaveRequest
        @param headers: GroupDepartSaveHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: GroupDepartSaveResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.GroupDepartSaveShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.sub_corp_id_list):
            request.sub_corp_id_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.sub_corp_id_list, 'sub_corp_id_list', 'json')
        body = {}
        if not UtilClient.is_unset(request.dept_name):
            body['dept_name'] = request.dept_name
        if not UtilClient.is_unset(request.manager_ids):
            body['manager_ids'] = request.manager_ids
        if not UtilClient.is_unset(request.outer_dept_id):
            body['outer_dept_id'] = request.outer_dept_id
        if not UtilClient.is_unset(request.outer_dept_pid):
            body['outer_dept_pid'] = request.outer_dept_pid
        if not UtilClient.is_unset(request.status):
            body['status'] = request.status
        if not UtilClient.is_unset(request.sub_corp_id_list_shrink):
            body['sub_corp_id_list'] = request.sub_corp_id_list_shrink
        if not UtilClient.is_unset(request.sync_group):
            body['sync_group'] = request.sync_group
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='GroupDepartSave',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/sub_corps/v1/departs',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.GroupDepartSaveResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def group_depart_save(
        self,
        request: btrip_open_20220520_models.GroupDepartSaveRequest,
    ) -> btrip_open_20220520_models.GroupDepartSaveResponse:
        """
        @summary 集团部门同步
        
        @param request: GroupDepartSaveRequest
        @return: GroupDepartSaveResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.GroupDepartSaveHeaders()
        return self.group_depart_save_with_options(request, headers, runtime)

    async def group_depart_save_async(
        self,
        request: btrip_open_20220520_models.GroupDepartSaveRequest,
    ) -> btrip_open_20220520_models.GroupDepartSaveResponse:
        """
        @summary 集团部门同步
        
        @param request: GroupDepartSaveRequest
        @return: GroupDepartSaveResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.GroupDepartSaveHeaders()
        return await self.group_depart_save_with_options_async(request, headers, runtime)

    def group_user_save_with_options(
        self,
        tmp_req: btrip_open_20220520_models.GroupUserSaveRequest,
        headers: btrip_open_20220520_models.GroupUserSaveHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.GroupUserSaveResponse:
        """
        @summary 集团人员同步
        
        @param tmp_req: GroupUserSaveRequest
        @param headers: GroupUserSaveHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: GroupUserSaveResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.GroupUserSaveShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.cert_list):
            request.cert_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.cert_list, 'cert_list', 'json')
        if not UtilClient.is_unset(tmp_req.sub_corp_id_list):
            request.sub_corp_id_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.sub_corp_id_list, 'sub_corp_id_list', 'json')
        body = {}
        if not UtilClient.is_unset(request.base_city_code):
            body['base_city_code'] = request.base_city_code
        if not UtilClient.is_unset(request.birthday):
            body['birthday'] = request.birthday
        if not UtilClient.is_unset(request.cert_list_shrink):
            body['cert_list'] = request.cert_list_shrink
        if not UtilClient.is_unset(request.gender):
            body['gender'] = request.gender
        if not UtilClient.is_unset(request.job_no):
            body['job_no'] = request.job_no
        if not UtilClient.is_unset(request.phone):
            body['phone'] = request.phone
        if not UtilClient.is_unset(request.real_name_en):
            body['real_name_en'] = request.real_name_en
        if not UtilClient.is_unset(request.sub_corp_id_list_shrink):
            body['sub_corp_id_list'] = request.sub_corp_id_list_shrink
        if not UtilClient.is_unset(request.user_id):
            body['user_id'] = request.user_id
        if not UtilClient.is_unset(request.user_name):
            body['user_name'] = request.user_name
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='GroupUserSave',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/sub_corps/v1/users',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.GroupUserSaveResponse(),
            self.call_api(params, req, runtime)
        )

    async def group_user_save_with_options_async(
        self,
        tmp_req: btrip_open_20220520_models.GroupUserSaveRequest,
        headers: btrip_open_20220520_models.GroupUserSaveHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.GroupUserSaveResponse:
        """
        @summary 集团人员同步
        
        @param tmp_req: GroupUserSaveRequest
        @param headers: GroupUserSaveHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: GroupUserSaveResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.GroupUserSaveShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.cert_list):
            request.cert_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.cert_list, 'cert_list', 'json')
        if not UtilClient.is_unset(tmp_req.sub_corp_id_list):
            request.sub_corp_id_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.sub_corp_id_list, 'sub_corp_id_list', 'json')
        body = {}
        if not UtilClient.is_unset(request.base_city_code):
            body['base_city_code'] = request.base_city_code
        if not UtilClient.is_unset(request.birthday):
            body['birthday'] = request.birthday
        if not UtilClient.is_unset(request.cert_list_shrink):
            body['cert_list'] = request.cert_list_shrink
        if not UtilClient.is_unset(request.gender):
            body['gender'] = request.gender
        if not UtilClient.is_unset(request.job_no):
            body['job_no'] = request.job_no
        if not UtilClient.is_unset(request.phone):
            body['phone'] = request.phone
        if not UtilClient.is_unset(request.real_name_en):
            body['real_name_en'] = request.real_name_en
        if not UtilClient.is_unset(request.sub_corp_id_list_shrink):
            body['sub_corp_id_list'] = request.sub_corp_id_list_shrink
        if not UtilClient.is_unset(request.user_id):
            body['user_id'] = request.user_id
        if not UtilClient.is_unset(request.user_name):
            body['user_name'] = request.user_name
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='GroupUserSave',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/sub_corps/v1/users',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.GroupUserSaveResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def group_user_save(
        self,
        request: btrip_open_20220520_models.GroupUserSaveRequest,
    ) -> btrip_open_20220520_models.GroupUserSaveResponse:
        """
        @summary 集团人员同步
        
        @param request: GroupUserSaveRequest
        @return: GroupUserSaveResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.GroupUserSaveHeaders()
        return self.group_user_save_with_options(request, headers, runtime)

    async def group_user_save_async(
        self,
        request: btrip_open_20220520_models.GroupUserSaveRequest,
    ) -> btrip_open_20220520_models.GroupUserSaveResponse:
        """
        @summary 集团人员同步
        
        @param request: GroupUserSaveRequest
        @return: GroupUserSaveResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.GroupUserSaveHeaders()
        return await self.group_user_save_with_options_async(request, headers, runtime)

    def hotel_asking_price_with_options(
        self,
        tmp_req: btrip_open_20220520_models.HotelAskingPriceRequest,
        headers: btrip_open_20220520_models.HotelAskingPriceHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.HotelAskingPriceResponse:
        """
        @summary 酒店起价
        
        @param tmp_req: HotelAskingPriceRequest
        @param headers: HotelAskingPriceHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: HotelAskingPriceResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.HotelAskingPriceShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.shids):
            request.shids_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.shids, 'shids', 'json')
        query = {}
        if not UtilClient.is_unset(request.adult_num):
            query['adult_num'] = request.adult_num
        if not UtilClient.is_unset(request.btrip_user_id):
            query['btrip_user_id'] = request.btrip_user_id
        if not UtilClient.is_unset(request.check_in_date):
            query['check_in_date'] = request.check_in_date
        if not UtilClient.is_unset(request.check_out_date):
            query['check_out_date'] = request.check_out_date
        if not UtilClient.is_unset(request.city_code):
            query['city_code'] = request.city_code
        if not UtilClient.is_unset(request.city_name):
            query['city_name'] = request.city_name
        if not UtilClient.is_unset(request.dir):
            query['dir'] = request.dir
        if not UtilClient.is_unset(request.hotel_star):
            query['hotel_star'] = request.hotel_star
        if not UtilClient.is_unset(request.is_protocol):
            query['is_protocol'] = request.is_protocol
        if not UtilClient.is_unset(request.payment_type):
            query['payment_type'] = request.payment_type
        if not UtilClient.is_unset(request.shids_shrink):
            query['shids'] = request.shids_shrink
        if not UtilClient.is_unset(request.sort_code):
            query['sort_code'] = request.sort_code
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='HotelAskingPrice',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-hotel/v1/hotels/action/asking-price',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.HotelAskingPriceResponse(),
            self.call_api(params, req, runtime)
        )

    async def hotel_asking_price_with_options_async(
        self,
        tmp_req: btrip_open_20220520_models.HotelAskingPriceRequest,
        headers: btrip_open_20220520_models.HotelAskingPriceHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.HotelAskingPriceResponse:
        """
        @summary 酒店起价
        
        @param tmp_req: HotelAskingPriceRequest
        @param headers: HotelAskingPriceHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: HotelAskingPriceResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.HotelAskingPriceShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.shids):
            request.shids_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.shids, 'shids', 'json')
        query = {}
        if not UtilClient.is_unset(request.adult_num):
            query['adult_num'] = request.adult_num
        if not UtilClient.is_unset(request.btrip_user_id):
            query['btrip_user_id'] = request.btrip_user_id
        if not UtilClient.is_unset(request.check_in_date):
            query['check_in_date'] = request.check_in_date
        if not UtilClient.is_unset(request.check_out_date):
            query['check_out_date'] = request.check_out_date
        if not UtilClient.is_unset(request.city_code):
            query['city_code'] = request.city_code
        if not UtilClient.is_unset(request.city_name):
            query['city_name'] = request.city_name
        if not UtilClient.is_unset(request.dir):
            query['dir'] = request.dir
        if not UtilClient.is_unset(request.hotel_star):
            query['hotel_star'] = request.hotel_star
        if not UtilClient.is_unset(request.is_protocol):
            query['is_protocol'] = request.is_protocol
        if not UtilClient.is_unset(request.payment_type):
            query['payment_type'] = request.payment_type
        if not UtilClient.is_unset(request.shids_shrink):
            query['shids'] = request.shids_shrink
        if not UtilClient.is_unset(request.sort_code):
            query['sort_code'] = request.sort_code
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='HotelAskingPrice',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-hotel/v1/hotels/action/asking-price',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.HotelAskingPriceResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def hotel_asking_price(
        self,
        request: btrip_open_20220520_models.HotelAskingPriceRequest,
    ) -> btrip_open_20220520_models.HotelAskingPriceResponse:
        """
        @summary 酒店起价
        
        @param request: HotelAskingPriceRequest
        @return: HotelAskingPriceResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.HotelAskingPriceHeaders()
        return self.hotel_asking_price_with_options(request, headers, runtime)

    async def hotel_asking_price_async(
        self,
        request: btrip_open_20220520_models.HotelAskingPriceRequest,
    ) -> btrip_open_20220520_models.HotelAskingPriceResponse:
        """
        @summary 酒店起价
        
        @param request: HotelAskingPriceRequest
        @return: HotelAskingPriceResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.HotelAskingPriceHeaders()
        return await self.hotel_asking_price_with_options_async(request, headers, runtime)

    def hotel_bill_settlement_query_with_options(
        self,
        request: btrip_open_20220520_models.HotelBillSettlementQueryRequest,
        headers: btrip_open_20220520_models.HotelBillSettlementQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.HotelBillSettlementQueryResponse:
        """
        @summary 查询酒店记账数据
        
        @param request: HotelBillSettlementQueryRequest
        @param headers: HotelBillSettlementQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: HotelBillSettlementQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.page_no):
            query['page_no'] = request.page_no
        if not UtilClient.is_unset(request.page_size):
            query['page_size'] = request.page_size
        if not UtilClient.is_unset(request.period_end):
            query['period_end'] = request.period_end
        if not UtilClient.is_unset(request.period_start):
            query['period_start'] = request.period_start
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='HotelBillSettlementQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/hotel/v1/bill-settlement',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.HotelBillSettlementQueryResponse(),
            self.call_api(params, req, runtime)
        )

    async def hotel_bill_settlement_query_with_options_async(
        self,
        request: btrip_open_20220520_models.HotelBillSettlementQueryRequest,
        headers: btrip_open_20220520_models.HotelBillSettlementQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.HotelBillSettlementQueryResponse:
        """
        @summary 查询酒店记账数据
        
        @param request: HotelBillSettlementQueryRequest
        @param headers: HotelBillSettlementQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: HotelBillSettlementQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.page_no):
            query['page_no'] = request.page_no
        if not UtilClient.is_unset(request.page_size):
            query['page_size'] = request.page_size
        if not UtilClient.is_unset(request.period_end):
            query['period_end'] = request.period_end
        if not UtilClient.is_unset(request.period_start):
            query['period_start'] = request.period_start
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='HotelBillSettlementQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/hotel/v1/bill-settlement',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.HotelBillSettlementQueryResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def hotel_bill_settlement_query(
        self,
        request: btrip_open_20220520_models.HotelBillSettlementQueryRequest,
    ) -> btrip_open_20220520_models.HotelBillSettlementQueryResponse:
        """
        @summary 查询酒店记账数据
        
        @param request: HotelBillSettlementQueryRequest
        @return: HotelBillSettlementQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.HotelBillSettlementQueryHeaders()
        return self.hotel_bill_settlement_query_with_options(request, headers, runtime)

    async def hotel_bill_settlement_query_async(
        self,
        request: btrip_open_20220520_models.HotelBillSettlementQueryRequest,
    ) -> btrip_open_20220520_models.HotelBillSettlementQueryResponse:
        """
        @summary 查询酒店记账数据
        
        @param request: HotelBillSettlementQueryRequest
        @return: HotelBillSettlementQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.HotelBillSettlementQueryHeaders()
        return await self.hotel_bill_settlement_query_with_options_async(request, headers, runtime)

    def hotel_city_code_list_with_options(
        self,
        request: btrip_open_20220520_models.HotelCityCodeListRequest,
        headers: btrip_open_20220520_models.HotelCityCodeListHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.HotelCityCodeListResponse:
        """
        @summary 酒店城市列表
        
        @param request: HotelCityCodeListRequest
        @param headers: HotelCityCodeListHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: HotelCityCodeListResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.country_code):
            query['country_code'] = request.country_code
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='HotelCityCodeList',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-hotel/v1/city-codes/action/search',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.HotelCityCodeListResponse(),
            self.call_api(params, req, runtime)
        )

    async def hotel_city_code_list_with_options_async(
        self,
        request: btrip_open_20220520_models.HotelCityCodeListRequest,
        headers: btrip_open_20220520_models.HotelCityCodeListHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.HotelCityCodeListResponse:
        """
        @summary 酒店城市列表
        
        @param request: HotelCityCodeListRequest
        @param headers: HotelCityCodeListHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: HotelCityCodeListResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.country_code):
            query['country_code'] = request.country_code
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='HotelCityCodeList',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-hotel/v1/city-codes/action/search',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.HotelCityCodeListResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def hotel_city_code_list(
        self,
        request: btrip_open_20220520_models.HotelCityCodeListRequest,
    ) -> btrip_open_20220520_models.HotelCityCodeListResponse:
        """
        @summary 酒店城市列表
        
        @param request: HotelCityCodeListRequest
        @return: HotelCityCodeListResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.HotelCityCodeListHeaders()
        return self.hotel_city_code_list_with_options(request, headers, runtime)

    async def hotel_city_code_list_async(
        self,
        request: btrip_open_20220520_models.HotelCityCodeListRequest,
    ) -> btrip_open_20220520_models.HotelCityCodeListResponse:
        """
        @summary 酒店城市列表
        
        @param request: HotelCityCodeListRequest
        @return: HotelCityCodeListResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.HotelCityCodeListHeaders()
        return await self.hotel_city_code_list_with_options_async(request, headers, runtime)

    def hotel_exceed_apply_query_with_options(
        self,
        request: btrip_open_20220520_models.HotelExceedApplyQueryRequest,
        headers: btrip_open_20220520_models.HotelExceedApplyQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.HotelExceedApplyQueryResponse:
        """
        @summary 查询酒店超标审批详情
        
        @param request: HotelExceedApplyQueryRequest
        @param headers: HotelExceedApplyQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: HotelExceedApplyQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.apply_id):
            query['apply_id'] = request.apply_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='HotelExceedApplyQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/apply/v1/hotel-exceed',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.HotelExceedApplyQueryResponse(),
            self.call_api(params, req, runtime)
        )

    async def hotel_exceed_apply_query_with_options_async(
        self,
        request: btrip_open_20220520_models.HotelExceedApplyQueryRequest,
        headers: btrip_open_20220520_models.HotelExceedApplyQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.HotelExceedApplyQueryResponse:
        """
        @summary 查询酒店超标审批详情
        
        @param request: HotelExceedApplyQueryRequest
        @param headers: HotelExceedApplyQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: HotelExceedApplyQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.apply_id):
            query['apply_id'] = request.apply_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='HotelExceedApplyQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/apply/v1/hotel-exceed',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.HotelExceedApplyQueryResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def hotel_exceed_apply_query(
        self,
        request: btrip_open_20220520_models.HotelExceedApplyQueryRequest,
    ) -> btrip_open_20220520_models.HotelExceedApplyQueryResponse:
        """
        @summary 查询酒店超标审批详情
        
        @param request: HotelExceedApplyQueryRequest
        @return: HotelExceedApplyQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.HotelExceedApplyQueryHeaders()
        return self.hotel_exceed_apply_query_with_options(request, headers, runtime)

    async def hotel_exceed_apply_query_async(
        self,
        request: btrip_open_20220520_models.HotelExceedApplyQueryRequest,
    ) -> btrip_open_20220520_models.HotelExceedApplyQueryResponse:
        """
        @summary 查询酒店超标审批详情
        
        @param request: HotelExceedApplyQueryRequest
        @return: HotelExceedApplyQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.HotelExceedApplyQueryHeaders()
        return await self.hotel_exceed_apply_query_with_options_async(request, headers, runtime)

    def hotel_goods_query_with_options(
        self,
        request: btrip_open_20220520_models.HotelGoodsQueryRequest,
        headers: btrip_open_20220520_models.HotelGoodsQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.HotelGoodsQueryResponse:
        """
        @summary 酒店详情页报价接口(直连)
        
        @param request: HotelGoodsQueryRequest
        @param headers: HotelGoodsQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: HotelGoodsQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.adult_num):
            query['adult_num'] = request.adult_num
        if not UtilClient.is_unset(request.agreement_price):
            query['agreement_price'] = request.agreement_price
        if not UtilClient.is_unset(request.begin_date):
            query['begin_date'] = request.begin_date
        if not UtilClient.is_unset(request.breakfast_included):
            query['breakfast_included'] = request.breakfast_included
        if not UtilClient.is_unset(request.btrip_user_id):
            query['btrip_user_id'] = request.btrip_user_id
        if not UtilClient.is_unset(request.city_code):
            query['city_code'] = request.city_code
        if not UtilClient.is_unset(request.end_date):
            query['end_date'] = request.end_date
        if not UtilClient.is_unset(request.hotel_id):
            query['hotel_id'] = request.hotel_id
        if not UtilClient.is_unset(request.pay_over_type):
            query['pay_over_type'] = request.pay_over_type
        if not UtilClient.is_unset(request.payment_type):
            query['payment_type'] = request.payment_type
        if not UtilClient.is_unset(request.special_invoice):
            query['special_invoice'] = request.special_invoice
        if not UtilClient.is_unset(request.super_man):
            query['super_man'] = request.super_man
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='HotelGoodsQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-hotel/v1/hotel-goods',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.HotelGoodsQueryResponse(),
            self.call_api(params, req, runtime)
        )

    async def hotel_goods_query_with_options_async(
        self,
        request: btrip_open_20220520_models.HotelGoodsQueryRequest,
        headers: btrip_open_20220520_models.HotelGoodsQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.HotelGoodsQueryResponse:
        """
        @summary 酒店详情页报价接口(直连)
        
        @param request: HotelGoodsQueryRequest
        @param headers: HotelGoodsQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: HotelGoodsQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.adult_num):
            query['adult_num'] = request.adult_num
        if not UtilClient.is_unset(request.agreement_price):
            query['agreement_price'] = request.agreement_price
        if not UtilClient.is_unset(request.begin_date):
            query['begin_date'] = request.begin_date
        if not UtilClient.is_unset(request.breakfast_included):
            query['breakfast_included'] = request.breakfast_included
        if not UtilClient.is_unset(request.btrip_user_id):
            query['btrip_user_id'] = request.btrip_user_id
        if not UtilClient.is_unset(request.city_code):
            query['city_code'] = request.city_code
        if not UtilClient.is_unset(request.end_date):
            query['end_date'] = request.end_date
        if not UtilClient.is_unset(request.hotel_id):
            query['hotel_id'] = request.hotel_id
        if not UtilClient.is_unset(request.pay_over_type):
            query['pay_over_type'] = request.pay_over_type
        if not UtilClient.is_unset(request.payment_type):
            query['payment_type'] = request.payment_type
        if not UtilClient.is_unset(request.special_invoice):
            query['special_invoice'] = request.special_invoice
        if not UtilClient.is_unset(request.super_man):
            query['super_man'] = request.super_man
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='HotelGoodsQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-hotel/v1/hotel-goods',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.HotelGoodsQueryResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def hotel_goods_query(
        self,
        request: btrip_open_20220520_models.HotelGoodsQueryRequest,
    ) -> btrip_open_20220520_models.HotelGoodsQueryResponse:
        """
        @summary 酒店详情页报价接口(直连)
        
        @param request: HotelGoodsQueryRequest
        @return: HotelGoodsQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.HotelGoodsQueryHeaders()
        return self.hotel_goods_query_with_options(request, headers, runtime)

    async def hotel_goods_query_async(
        self,
        request: btrip_open_20220520_models.HotelGoodsQueryRequest,
    ) -> btrip_open_20220520_models.HotelGoodsQueryResponse:
        """
        @summary 酒店详情页报价接口(直连)
        
        @param request: HotelGoodsQueryRequest
        @return: HotelGoodsQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.HotelGoodsQueryHeaders()
        return await self.hotel_goods_query_with_options_async(request, headers, runtime)

    def hotel_index_info_with_options(
        self,
        request: btrip_open_20220520_models.HotelIndexInfoRequest,
        headers: btrip_open_20220520_models.HotelIndexInfoHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.HotelIndexInfoResponse:
        """
        @summary 获取酒店清单
        
        @param request: HotelIndexInfoRequest
        @param headers: HotelIndexInfoHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: HotelIndexInfoResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.city_code):
            query['city_code'] = request.city_code
        if not UtilClient.is_unset(request.hotel_status):
            query['hotel_status'] = request.hotel_status
        if not UtilClient.is_unset(request.page_size):
            query['page_size'] = request.page_size
        if not UtilClient.is_unset(request.page_token):
            query['page_token'] = request.page_token
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='HotelIndexInfo',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-hotel/v1/index-infos',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.HotelIndexInfoResponse(),
            self.call_api(params, req, runtime)
        )

    async def hotel_index_info_with_options_async(
        self,
        request: btrip_open_20220520_models.HotelIndexInfoRequest,
        headers: btrip_open_20220520_models.HotelIndexInfoHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.HotelIndexInfoResponse:
        """
        @summary 获取酒店清单
        
        @param request: HotelIndexInfoRequest
        @param headers: HotelIndexInfoHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: HotelIndexInfoResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.city_code):
            query['city_code'] = request.city_code
        if not UtilClient.is_unset(request.hotel_status):
            query['hotel_status'] = request.hotel_status
        if not UtilClient.is_unset(request.page_size):
            query['page_size'] = request.page_size
        if not UtilClient.is_unset(request.page_token):
            query['page_token'] = request.page_token
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='HotelIndexInfo',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-hotel/v1/index-infos',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.HotelIndexInfoResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def hotel_index_info(
        self,
        request: btrip_open_20220520_models.HotelIndexInfoRequest,
    ) -> btrip_open_20220520_models.HotelIndexInfoResponse:
        """
        @summary 获取酒店清单
        
        @param request: HotelIndexInfoRequest
        @return: HotelIndexInfoResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.HotelIndexInfoHeaders()
        return self.hotel_index_info_with_options(request, headers, runtime)

    async def hotel_index_info_async(
        self,
        request: btrip_open_20220520_models.HotelIndexInfoRequest,
    ) -> btrip_open_20220520_models.HotelIndexInfoResponse:
        """
        @summary 获取酒店清单
        
        @param request: HotelIndexInfoRequest
        @return: HotelIndexInfoResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.HotelIndexInfoHeaders()
        return await self.hotel_index_info_with_options_async(request, headers, runtime)

    def hotel_order_cancel_with_options(
        self,
        request: btrip_open_20220520_models.HotelOrderCancelRequest,
        headers: btrip_open_20220520_models.HotelOrderCancelHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.HotelOrderCancelResponse:
        """
        @summary 酒店订单取消
        
        @param request: HotelOrderCancelRequest
        @param headers: HotelOrderCancelHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: HotelOrderCancelResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.btrip_order_id):
            query['btrip_order_id'] = request.btrip_order_id
        if not UtilClient.is_unset(request.dis_order_id):
            query['dis_order_id'] = request.dis_order_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='HotelOrderCancel',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-hotel/v1/orders/action/cancel',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.HotelOrderCancelResponse(),
            self.call_api(params, req, runtime)
        )

    async def hotel_order_cancel_with_options_async(
        self,
        request: btrip_open_20220520_models.HotelOrderCancelRequest,
        headers: btrip_open_20220520_models.HotelOrderCancelHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.HotelOrderCancelResponse:
        """
        @summary 酒店订单取消
        
        @param request: HotelOrderCancelRequest
        @param headers: HotelOrderCancelHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: HotelOrderCancelResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.btrip_order_id):
            query['btrip_order_id'] = request.btrip_order_id
        if not UtilClient.is_unset(request.dis_order_id):
            query['dis_order_id'] = request.dis_order_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='HotelOrderCancel',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-hotel/v1/orders/action/cancel',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.HotelOrderCancelResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def hotel_order_cancel(
        self,
        request: btrip_open_20220520_models.HotelOrderCancelRequest,
    ) -> btrip_open_20220520_models.HotelOrderCancelResponse:
        """
        @summary 酒店订单取消
        
        @param request: HotelOrderCancelRequest
        @return: HotelOrderCancelResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.HotelOrderCancelHeaders()
        return self.hotel_order_cancel_with_options(request, headers, runtime)

    async def hotel_order_cancel_async(
        self,
        request: btrip_open_20220520_models.HotelOrderCancelRequest,
    ) -> btrip_open_20220520_models.HotelOrderCancelResponse:
        """
        @summary 酒店订单取消
        
        @param request: HotelOrderCancelRequest
        @return: HotelOrderCancelResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.HotelOrderCancelHeaders()
        return await self.hotel_order_cancel_with_options_async(request, headers, runtime)

    def hotel_order_create_with_options(
        self,
        tmp_req: btrip_open_20220520_models.HotelOrderCreateRequest,
        headers: btrip_open_20220520_models.HotelOrderCreateHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.HotelOrderCreateResponse:
        """
        @summary 酒店订单创建
        
        @param tmp_req: HotelOrderCreateRequest
        @param headers: HotelOrderCreateHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: HotelOrderCreateResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.HotelOrderCreateShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.invoice_info):
            request.invoice_info_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.invoice_info, 'invoice_info', 'json')
        if not UtilClient.is_unset(tmp_req.occupant_info_list):
            request.occupant_info_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.occupant_info_list, 'occupant_info_list', 'json')
        if not UtilClient.is_unset(tmp_req.promotion_info):
            request.promotion_info_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.promotion_info, 'promotion_info', 'json')
        body = {}
        if not UtilClient.is_unset(request.btrip_user_id):
            body['btrip_user_id'] = request.btrip_user_id
        if not UtilClient.is_unset(request.check_in):
            body['check_in'] = request.check_in
        if not UtilClient.is_unset(request.check_out):
            body['check_out'] = request.check_out
        if not UtilClient.is_unset(request.contract_email):
            body['contract_email'] = request.contract_email
        if not UtilClient.is_unset(request.contract_name):
            body['contract_name'] = request.contract_name
        if not UtilClient.is_unset(request.contract_phone):
            body['contract_phone'] = request.contract_phone
        if not UtilClient.is_unset(request.corp_pay_price):
            body['corp_pay_price'] = request.corp_pay_price
        if not UtilClient.is_unset(request.dis_order_id):
            body['dis_order_id'] = request.dis_order_id
        if not UtilClient.is_unset(request.extra):
            body['extra'] = request.extra
        if not UtilClient.is_unset(request.invoice_info_shrink):
            body['invoice_info'] = request.invoice_info_shrink
        if not UtilClient.is_unset(request.item_id):
            body['item_id'] = request.item_id
        if not UtilClient.is_unset(request.itinerary_no):
            body['itinerary_no'] = request.itinerary_no
        if not UtilClient.is_unset(request.occupant_info_list_shrink):
            body['occupant_info_list'] = request.occupant_info_list_shrink
        if not UtilClient.is_unset(request.person_pay_price):
            body['person_pay_price'] = request.person_pay_price
        if not UtilClient.is_unset(request.promotion_info_shrink):
            body['promotion_info'] = request.promotion_info_shrink
        if not UtilClient.is_unset(request.rate_plan_id):
            body['rate_plan_id'] = request.rate_plan_id
        if not UtilClient.is_unset(request.room_id):
            body['room_id'] = request.room_id
        if not UtilClient.is_unset(request.room_num):
            body['room_num'] = request.room_num
        if not UtilClient.is_unset(request.seller_id):
            body['seller_id'] = request.seller_id
        if not UtilClient.is_unset(request.shid):
            body['shid'] = request.shid
        if not UtilClient.is_unset(request.total_order_price):
            body['total_order_price'] = request.total_order_price
        if not UtilClient.is_unset(request.validate_res_key):
            body['validate_res_key'] = request.validate_res_key
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='HotelOrderCreate',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-hotel/v1/orders/action/create',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.HotelOrderCreateResponse(),
            self.call_api(params, req, runtime)
        )

    async def hotel_order_create_with_options_async(
        self,
        tmp_req: btrip_open_20220520_models.HotelOrderCreateRequest,
        headers: btrip_open_20220520_models.HotelOrderCreateHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.HotelOrderCreateResponse:
        """
        @summary 酒店订单创建
        
        @param tmp_req: HotelOrderCreateRequest
        @param headers: HotelOrderCreateHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: HotelOrderCreateResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.HotelOrderCreateShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.invoice_info):
            request.invoice_info_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.invoice_info, 'invoice_info', 'json')
        if not UtilClient.is_unset(tmp_req.occupant_info_list):
            request.occupant_info_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.occupant_info_list, 'occupant_info_list', 'json')
        if not UtilClient.is_unset(tmp_req.promotion_info):
            request.promotion_info_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.promotion_info, 'promotion_info', 'json')
        body = {}
        if not UtilClient.is_unset(request.btrip_user_id):
            body['btrip_user_id'] = request.btrip_user_id
        if not UtilClient.is_unset(request.check_in):
            body['check_in'] = request.check_in
        if not UtilClient.is_unset(request.check_out):
            body['check_out'] = request.check_out
        if not UtilClient.is_unset(request.contract_email):
            body['contract_email'] = request.contract_email
        if not UtilClient.is_unset(request.contract_name):
            body['contract_name'] = request.contract_name
        if not UtilClient.is_unset(request.contract_phone):
            body['contract_phone'] = request.contract_phone
        if not UtilClient.is_unset(request.corp_pay_price):
            body['corp_pay_price'] = request.corp_pay_price
        if not UtilClient.is_unset(request.dis_order_id):
            body['dis_order_id'] = request.dis_order_id
        if not UtilClient.is_unset(request.extra):
            body['extra'] = request.extra
        if not UtilClient.is_unset(request.invoice_info_shrink):
            body['invoice_info'] = request.invoice_info_shrink
        if not UtilClient.is_unset(request.item_id):
            body['item_id'] = request.item_id
        if not UtilClient.is_unset(request.itinerary_no):
            body['itinerary_no'] = request.itinerary_no
        if not UtilClient.is_unset(request.occupant_info_list_shrink):
            body['occupant_info_list'] = request.occupant_info_list_shrink
        if not UtilClient.is_unset(request.person_pay_price):
            body['person_pay_price'] = request.person_pay_price
        if not UtilClient.is_unset(request.promotion_info_shrink):
            body['promotion_info'] = request.promotion_info_shrink
        if not UtilClient.is_unset(request.rate_plan_id):
            body['rate_plan_id'] = request.rate_plan_id
        if not UtilClient.is_unset(request.room_id):
            body['room_id'] = request.room_id
        if not UtilClient.is_unset(request.room_num):
            body['room_num'] = request.room_num
        if not UtilClient.is_unset(request.seller_id):
            body['seller_id'] = request.seller_id
        if not UtilClient.is_unset(request.shid):
            body['shid'] = request.shid
        if not UtilClient.is_unset(request.total_order_price):
            body['total_order_price'] = request.total_order_price
        if not UtilClient.is_unset(request.validate_res_key):
            body['validate_res_key'] = request.validate_res_key
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='HotelOrderCreate',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-hotel/v1/orders/action/create',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.HotelOrderCreateResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def hotel_order_create(
        self,
        request: btrip_open_20220520_models.HotelOrderCreateRequest,
    ) -> btrip_open_20220520_models.HotelOrderCreateResponse:
        """
        @summary 酒店订单创建
        
        @param request: HotelOrderCreateRequest
        @return: HotelOrderCreateResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.HotelOrderCreateHeaders()
        return self.hotel_order_create_with_options(request, headers, runtime)

    async def hotel_order_create_async(
        self,
        request: btrip_open_20220520_models.HotelOrderCreateRequest,
    ) -> btrip_open_20220520_models.HotelOrderCreateResponse:
        """
        @summary 酒店订单创建
        
        @param request: HotelOrderCreateRequest
        @return: HotelOrderCreateResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.HotelOrderCreateHeaders()
        return await self.hotel_order_create_with_options_async(request, headers, runtime)

    def hotel_order_detail_info_with_options(
        self,
        request: btrip_open_20220520_models.HotelOrderDetailInfoRequest,
        headers: btrip_open_20220520_models.HotelOrderDetailInfoHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.HotelOrderDetailInfoResponse:
        """
        @summary 酒店订单明细信息
        
        @param request: HotelOrderDetailInfoRequest
        @param headers: HotelOrderDetailInfoHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: HotelOrderDetailInfoResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.btrip_order_id):
            query['btrip_order_id'] = request.btrip_order_id
        if not UtilClient.is_unset(request.dis_order_id):
            query['dis_order_id'] = request.dis_order_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='HotelOrderDetailInfo',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-hotel/v1/orders/action/detail',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.HotelOrderDetailInfoResponse(),
            self.call_api(params, req, runtime)
        )

    async def hotel_order_detail_info_with_options_async(
        self,
        request: btrip_open_20220520_models.HotelOrderDetailInfoRequest,
        headers: btrip_open_20220520_models.HotelOrderDetailInfoHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.HotelOrderDetailInfoResponse:
        """
        @summary 酒店订单明细信息
        
        @param request: HotelOrderDetailInfoRequest
        @param headers: HotelOrderDetailInfoHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: HotelOrderDetailInfoResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.btrip_order_id):
            query['btrip_order_id'] = request.btrip_order_id
        if not UtilClient.is_unset(request.dis_order_id):
            query['dis_order_id'] = request.dis_order_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='HotelOrderDetailInfo',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-hotel/v1/orders/action/detail',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.HotelOrderDetailInfoResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def hotel_order_detail_info(
        self,
        request: btrip_open_20220520_models.HotelOrderDetailInfoRequest,
    ) -> btrip_open_20220520_models.HotelOrderDetailInfoResponse:
        """
        @summary 酒店订单明细信息
        
        @param request: HotelOrderDetailInfoRequest
        @return: HotelOrderDetailInfoResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.HotelOrderDetailInfoHeaders()
        return self.hotel_order_detail_info_with_options(request, headers, runtime)

    async def hotel_order_detail_info_async(
        self,
        request: btrip_open_20220520_models.HotelOrderDetailInfoRequest,
    ) -> btrip_open_20220520_models.HotelOrderDetailInfoResponse:
        """
        @summary 酒店订单明细信息
        
        @param request: HotelOrderDetailInfoRequest
        @return: HotelOrderDetailInfoResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.HotelOrderDetailInfoHeaders()
        return await self.hotel_order_detail_info_with_options_async(request, headers, runtime)

    def hotel_order_list_query_with_options(
        self,
        request: btrip_open_20220520_models.HotelOrderListQueryRequest,
        headers: btrip_open_20220520_models.HotelOrderListQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.HotelOrderListQueryResponse:
        """
        @summary 查询酒店订单列表
        
        @param request: HotelOrderListQueryRequest
        @param headers: HotelOrderListQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: HotelOrderListQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.all_apply):
            query['all_apply'] = request.all_apply
        if not UtilClient.is_unset(request.apply_id):
            query['apply_id'] = request.apply_id
        if not UtilClient.is_unset(request.depart_id):
            query['depart_id'] = request.depart_id
        if not UtilClient.is_unset(request.end_time):
            query['end_time'] = request.end_time
        if not UtilClient.is_unset(request.page):
            query['page'] = request.page
        if not UtilClient.is_unset(request.page_size):
            query['page_size'] = request.page_size
        if not UtilClient.is_unset(request.start_time):
            query['start_time'] = request.start_time
        if not UtilClient.is_unset(request.thirdpart_apply_id):
            query['thirdpart_apply_id'] = request.thirdpart_apply_id
        if not UtilClient.is_unset(request.update_end_time):
            query['update_end_time'] = request.update_end_time
        if not UtilClient.is_unset(request.update_start_time):
            query['update_start_time'] = request.update_start_time
        if not UtilClient.is_unset(request.user_id):
            query['user_id'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='HotelOrderListQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/hotel/v1/order-list',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.HotelOrderListQueryResponse(),
            self.call_api(params, req, runtime)
        )

    async def hotel_order_list_query_with_options_async(
        self,
        request: btrip_open_20220520_models.HotelOrderListQueryRequest,
        headers: btrip_open_20220520_models.HotelOrderListQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.HotelOrderListQueryResponse:
        """
        @summary 查询酒店订单列表
        
        @param request: HotelOrderListQueryRequest
        @param headers: HotelOrderListQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: HotelOrderListQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.all_apply):
            query['all_apply'] = request.all_apply
        if not UtilClient.is_unset(request.apply_id):
            query['apply_id'] = request.apply_id
        if not UtilClient.is_unset(request.depart_id):
            query['depart_id'] = request.depart_id
        if not UtilClient.is_unset(request.end_time):
            query['end_time'] = request.end_time
        if not UtilClient.is_unset(request.page):
            query['page'] = request.page
        if not UtilClient.is_unset(request.page_size):
            query['page_size'] = request.page_size
        if not UtilClient.is_unset(request.start_time):
            query['start_time'] = request.start_time
        if not UtilClient.is_unset(request.thirdpart_apply_id):
            query['thirdpart_apply_id'] = request.thirdpart_apply_id
        if not UtilClient.is_unset(request.update_end_time):
            query['update_end_time'] = request.update_end_time
        if not UtilClient.is_unset(request.update_start_time):
            query['update_start_time'] = request.update_start_time
        if not UtilClient.is_unset(request.user_id):
            query['user_id'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='HotelOrderListQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/hotel/v1/order-list',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.HotelOrderListQueryResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def hotel_order_list_query(
        self,
        request: btrip_open_20220520_models.HotelOrderListQueryRequest,
    ) -> btrip_open_20220520_models.HotelOrderListQueryResponse:
        """
        @summary 查询酒店订单列表
        
        @param request: HotelOrderListQueryRequest
        @return: HotelOrderListQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.HotelOrderListQueryHeaders()
        return self.hotel_order_list_query_with_options(request, headers, runtime)

    async def hotel_order_list_query_async(
        self,
        request: btrip_open_20220520_models.HotelOrderListQueryRequest,
    ) -> btrip_open_20220520_models.HotelOrderListQueryResponse:
        """
        @summary 查询酒店订单列表
        
        @param request: HotelOrderListQueryRequest
        @return: HotelOrderListQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.HotelOrderListQueryHeaders()
        return await self.hotel_order_list_query_with_options_async(request, headers, runtime)

    def hotel_order_pay_with_options(
        self,
        request: btrip_open_20220520_models.HotelOrderPayRequest,
        headers: btrip_open_20220520_models.HotelOrderPayHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.HotelOrderPayResponse:
        """
        @summary 酒店订单支付
        
        @param request: HotelOrderPayRequest
        @param headers: HotelOrderPayHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: HotelOrderPayResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.btrip_order_id):
            body['btrip_order_id'] = request.btrip_order_id
        if not UtilClient.is_unset(request.btrip_user_id):
            body['btrip_user_id'] = request.btrip_user_id
        if not UtilClient.is_unset(request.company_pay_fee):
            body['company_pay_fee'] = request.company_pay_fee
        if not UtilClient.is_unset(request.person_pay_fee):
            body['person_pay_fee'] = request.person_pay_fee
        if not UtilClient.is_unset(request.third_pay_account):
            body['third_pay_account'] = request.third_pay_account
        if not UtilClient.is_unset(request.third_trade_no):
            body['third_trade_no'] = request.third_trade_no
        if not UtilClient.is_unset(request.total_price):
            body['total_price'] = request.total_price
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='HotelOrderPay',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-hotel/v1/orders/action/pay',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.HotelOrderPayResponse(),
            self.call_api(params, req, runtime)
        )

    async def hotel_order_pay_with_options_async(
        self,
        request: btrip_open_20220520_models.HotelOrderPayRequest,
        headers: btrip_open_20220520_models.HotelOrderPayHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.HotelOrderPayResponse:
        """
        @summary 酒店订单支付
        
        @param request: HotelOrderPayRequest
        @param headers: HotelOrderPayHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: HotelOrderPayResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.btrip_order_id):
            body['btrip_order_id'] = request.btrip_order_id
        if not UtilClient.is_unset(request.btrip_user_id):
            body['btrip_user_id'] = request.btrip_user_id
        if not UtilClient.is_unset(request.company_pay_fee):
            body['company_pay_fee'] = request.company_pay_fee
        if not UtilClient.is_unset(request.person_pay_fee):
            body['person_pay_fee'] = request.person_pay_fee
        if not UtilClient.is_unset(request.third_pay_account):
            body['third_pay_account'] = request.third_pay_account
        if not UtilClient.is_unset(request.third_trade_no):
            body['third_trade_no'] = request.third_trade_no
        if not UtilClient.is_unset(request.total_price):
            body['total_price'] = request.total_price
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='HotelOrderPay',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-hotel/v1/orders/action/pay',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.HotelOrderPayResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def hotel_order_pay(
        self,
        request: btrip_open_20220520_models.HotelOrderPayRequest,
    ) -> btrip_open_20220520_models.HotelOrderPayResponse:
        """
        @summary 酒店订单支付
        
        @param request: HotelOrderPayRequest
        @return: HotelOrderPayResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.HotelOrderPayHeaders()
        return self.hotel_order_pay_with_options(request, headers, runtime)

    async def hotel_order_pay_async(
        self,
        request: btrip_open_20220520_models.HotelOrderPayRequest,
    ) -> btrip_open_20220520_models.HotelOrderPayResponse:
        """
        @summary 酒店订单支付
        
        @param request: HotelOrderPayRequest
        @return: HotelOrderPayResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.HotelOrderPayHeaders()
        return await self.hotel_order_pay_with_options_async(request, headers, runtime)

    def hotel_order_pre_validate_with_options(
        self,
        tmp_req: btrip_open_20220520_models.HotelOrderPreValidateRequest,
        headers: btrip_open_20220520_models.HotelOrderPreValidateHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.HotelOrderPreValidateResponse:
        """
        @summary 酒店下单前校验
        
        @param tmp_req: HotelOrderPreValidateRequest
        @param headers: HotelOrderPreValidateHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: HotelOrderPreValidateResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.HotelOrderPreValidateShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.daily_list):
            request.daily_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.daily_list, 'daily_list', 'json')
        if not UtilClient.is_unset(tmp_req.occupant_info_list):
            request.occupant_info_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.occupant_info_list, 'occupant_info_list', 'json')
        query = {}
        if not UtilClient.is_unset(request.btrip_user_id):
            query['btrip_user_id'] = request.btrip_user_id
        if not UtilClient.is_unset(request.check_in):
            query['check_in'] = request.check_in
        if not UtilClient.is_unset(request.check_out):
            query['check_out'] = request.check_out
        if not UtilClient.is_unset(request.daily_list_shrink):
            query['daily_list'] = request.daily_list_shrink
        if not UtilClient.is_unset(request.item_id):
            query['item_id'] = request.item_id
        if not UtilClient.is_unset(request.number_of_adults_per_room):
            query['number_of_adults_per_room'] = request.number_of_adults_per_room
        if not UtilClient.is_unset(request.occupant_info_list_shrink):
            query['occupant_info_list'] = request.occupant_info_list_shrink
        if not UtilClient.is_unset(request.rate_plan_id):
            query['rate_plan_id'] = request.rate_plan_id
        if not UtilClient.is_unset(request.room_id):
            query['room_id'] = request.room_id
        if not UtilClient.is_unset(request.room_num):
            query['room_num'] = request.room_num
        if not UtilClient.is_unset(request.search_room_price):
            query['search_room_price'] = request.search_room_price
        if not UtilClient.is_unset(request.seller_id):
            query['seller_id'] = request.seller_id
        if not UtilClient.is_unset(request.shid):
            query['shid'] = request.shid
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='HotelOrderPreValidate',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-hotel/v1/orders/action/pre-validate',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.HotelOrderPreValidateResponse(),
            self.call_api(params, req, runtime)
        )

    async def hotel_order_pre_validate_with_options_async(
        self,
        tmp_req: btrip_open_20220520_models.HotelOrderPreValidateRequest,
        headers: btrip_open_20220520_models.HotelOrderPreValidateHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.HotelOrderPreValidateResponse:
        """
        @summary 酒店下单前校验
        
        @param tmp_req: HotelOrderPreValidateRequest
        @param headers: HotelOrderPreValidateHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: HotelOrderPreValidateResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.HotelOrderPreValidateShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.daily_list):
            request.daily_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.daily_list, 'daily_list', 'json')
        if not UtilClient.is_unset(tmp_req.occupant_info_list):
            request.occupant_info_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.occupant_info_list, 'occupant_info_list', 'json')
        query = {}
        if not UtilClient.is_unset(request.btrip_user_id):
            query['btrip_user_id'] = request.btrip_user_id
        if not UtilClient.is_unset(request.check_in):
            query['check_in'] = request.check_in
        if not UtilClient.is_unset(request.check_out):
            query['check_out'] = request.check_out
        if not UtilClient.is_unset(request.daily_list_shrink):
            query['daily_list'] = request.daily_list_shrink
        if not UtilClient.is_unset(request.item_id):
            query['item_id'] = request.item_id
        if not UtilClient.is_unset(request.number_of_adults_per_room):
            query['number_of_adults_per_room'] = request.number_of_adults_per_room
        if not UtilClient.is_unset(request.occupant_info_list_shrink):
            query['occupant_info_list'] = request.occupant_info_list_shrink
        if not UtilClient.is_unset(request.rate_plan_id):
            query['rate_plan_id'] = request.rate_plan_id
        if not UtilClient.is_unset(request.room_id):
            query['room_id'] = request.room_id
        if not UtilClient.is_unset(request.room_num):
            query['room_num'] = request.room_num
        if not UtilClient.is_unset(request.search_room_price):
            query['search_room_price'] = request.search_room_price
        if not UtilClient.is_unset(request.seller_id):
            query['seller_id'] = request.seller_id
        if not UtilClient.is_unset(request.shid):
            query['shid'] = request.shid
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='HotelOrderPreValidate',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-hotel/v1/orders/action/pre-validate',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.HotelOrderPreValidateResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def hotel_order_pre_validate(
        self,
        request: btrip_open_20220520_models.HotelOrderPreValidateRequest,
    ) -> btrip_open_20220520_models.HotelOrderPreValidateResponse:
        """
        @summary 酒店下单前校验
        
        @param request: HotelOrderPreValidateRequest
        @return: HotelOrderPreValidateResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.HotelOrderPreValidateHeaders()
        return self.hotel_order_pre_validate_with_options(request, headers, runtime)

    async def hotel_order_pre_validate_async(
        self,
        request: btrip_open_20220520_models.HotelOrderPreValidateRequest,
    ) -> btrip_open_20220520_models.HotelOrderPreValidateResponse:
        """
        @summary 酒店下单前校验
        
        @param request: HotelOrderPreValidateRequest
        @return: HotelOrderPreValidateResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.HotelOrderPreValidateHeaders()
        return await self.hotel_order_pre_validate_with_options_async(request, headers, runtime)

    def hotel_order_query_with_options(
        self,
        request: btrip_open_20220520_models.HotelOrderQueryRequest,
        headers: btrip_open_20220520_models.HotelOrderQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.HotelOrderQueryResponse:
        """
        @summary 酒店订单查询
        
        @param request: HotelOrderQueryRequest
        @param headers: HotelOrderQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: HotelOrderQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.order_id):
            query['order_id'] = request.order_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='HotelOrderQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/hotel/v1/order',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.HotelOrderQueryResponse(),
            self.call_api(params, req, runtime)
        )

    async def hotel_order_query_with_options_async(
        self,
        request: btrip_open_20220520_models.HotelOrderQueryRequest,
        headers: btrip_open_20220520_models.HotelOrderQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.HotelOrderQueryResponse:
        """
        @summary 酒店订单查询
        
        @param request: HotelOrderQueryRequest
        @param headers: HotelOrderQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: HotelOrderQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.order_id):
            query['order_id'] = request.order_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='HotelOrderQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/hotel/v1/order',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.HotelOrderQueryResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def hotel_order_query(
        self,
        request: btrip_open_20220520_models.HotelOrderQueryRequest,
    ) -> btrip_open_20220520_models.HotelOrderQueryResponse:
        """
        @summary 酒店订单查询
        
        @param request: HotelOrderQueryRequest
        @return: HotelOrderQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.HotelOrderQueryHeaders()
        return self.hotel_order_query_with_options(request, headers, runtime)

    async def hotel_order_query_async(
        self,
        request: btrip_open_20220520_models.HotelOrderQueryRequest,
    ) -> btrip_open_20220520_models.HotelOrderQueryResponse:
        """
        @summary 酒店订单查询
        
        @param request: HotelOrderQueryRequest
        @return: HotelOrderQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.HotelOrderQueryHeaders()
        return await self.hotel_order_query_with_options_async(request, headers, runtime)

    def hotel_price_pull_with_options(
        self,
        tmp_req: btrip_open_20220520_models.HotelPricePullRequest,
        headers: btrip_open_20220520_models.HotelPricePullHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.HotelPricePullResponse:
        """
        @summary 酒店拉动态拉取价格接口(落地)
        
        @param tmp_req: HotelPricePullRequest
        @param headers: HotelPricePullHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: HotelPricePullResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.HotelPricePullShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.hotel_ids):
            request.hotel_ids_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.hotel_ids, 'hotel_ids', 'json')
        query = {}
        if not UtilClient.is_unset(request.btrip_user_id):
            query['btrip_user_id'] = request.btrip_user_id
        if not UtilClient.is_unset(request.check_in):
            query['check_in'] = request.check_in
        if not UtilClient.is_unset(request.check_out):
            query['check_out'] = request.check_out
        if not UtilClient.is_unset(request.city_code):
            query['city_code'] = request.city_code
        if not UtilClient.is_unset(request.hotel_ids_shrink):
            query['hotel_ids'] = request.hotel_ids_shrink
        if not UtilClient.is_unset(request.payment_type):
            query['payment_type'] = request.payment_type
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='HotelPricePull',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-hotel/v1/prices/action/pull',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.HotelPricePullResponse(),
            self.call_api(params, req, runtime)
        )

    async def hotel_price_pull_with_options_async(
        self,
        tmp_req: btrip_open_20220520_models.HotelPricePullRequest,
        headers: btrip_open_20220520_models.HotelPricePullHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.HotelPricePullResponse:
        """
        @summary 酒店拉动态拉取价格接口(落地)
        
        @param tmp_req: HotelPricePullRequest
        @param headers: HotelPricePullHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: HotelPricePullResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.HotelPricePullShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.hotel_ids):
            request.hotel_ids_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.hotel_ids, 'hotel_ids', 'json')
        query = {}
        if not UtilClient.is_unset(request.btrip_user_id):
            query['btrip_user_id'] = request.btrip_user_id
        if not UtilClient.is_unset(request.check_in):
            query['check_in'] = request.check_in
        if not UtilClient.is_unset(request.check_out):
            query['check_out'] = request.check_out
        if not UtilClient.is_unset(request.city_code):
            query['city_code'] = request.city_code
        if not UtilClient.is_unset(request.hotel_ids_shrink):
            query['hotel_ids'] = request.hotel_ids_shrink
        if not UtilClient.is_unset(request.payment_type):
            query['payment_type'] = request.payment_type
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='HotelPricePull',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-hotel/v1/prices/action/pull',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.HotelPricePullResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def hotel_price_pull(
        self,
        request: btrip_open_20220520_models.HotelPricePullRequest,
    ) -> btrip_open_20220520_models.HotelPricePullResponse:
        """
        @summary 酒店拉动态拉取价格接口(落地)
        
        @param request: HotelPricePullRequest
        @return: HotelPricePullResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.HotelPricePullHeaders()
        return self.hotel_price_pull_with_options(request, headers, runtime)

    async def hotel_price_pull_async(
        self,
        request: btrip_open_20220520_models.HotelPricePullRequest,
    ) -> btrip_open_20220520_models.HotelPricePullResponse:
        """
        @summary 酒店拉动态拉取价格接口(落地)
        
        @param request: HotelPricePullRequest
        @return: HotelPricePullResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.HotelPricePullHeaders()
        return await self.hotel_price_pull_with_options_async(request, headers, runtime)

    def hotel_room_info_with_options(
        self,
        tmp_req: btrip_open_20220520_models.HotelRoomInfoRequest,
        headers: btrip_open_20220520_models.HotelRoomInfoHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.HotelRoomInfoResponse:
        """
        @summary 获取酒店静态房型详情
        
        @param tmp_req: HotelRoomInfoRequest
        @param headers: HotelRoomInfoHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: HotelRoomInfoResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.HotelRoomInfoShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.room_ids):
            request.room_ids_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.room_ids, 'room_ids', 'json')
        query = {}
        if not UtilClient.is_unset(request.room_ids_shrink):
            query['room_ids'] = request.room_ids_shrink
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='HotelRoomInfo',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-hotel/v1/room-infos',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.HotelRoomInfoResponse(),
            self.call_api(params, req, runtime)
        )

    async def hotel_room_info_with_options_async(
        self,
        tmp_req: btrip_open_20220520_models.HotelRoomInfoRequest,
        headers: btrip_open_20220520_models.HotelRoomInfoHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.HotelRoomInfoResponse:
        """
        @summary 获取酒店静态房型详情
        
        @param tmp_req: HotelRoomInfoRequest
        @param headers: HotelRoomInfoHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: HotelRoomInfoResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.HotelRoomInfoShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.room_ids):
            request.room_ids_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.room_ids, 'room_ids', 'json')
        query = {}
        if not UtilClient.is_unset(request.room_ids_shrink):
            query['room_ids'] = request.room_ids_shrink
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='HotelRoomInfo',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-hotel/v1/room-infos',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.HotelRoomInfoResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def hotel_room_info(
        self,
        request: btrip_open_20220520_models.HotelRoomInfoRequest,
    ) -> btrip_open_20220520_models.HotelRoomInfoResponse:
        """
        @summary 获取酒店静态房型详情
        
        @param request: HotelRoomInfoRequest
        @return: HotelRoomInfoResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.HotelRoomInfoHeaders()
        return self.hotel_room_info_with_options(request, headers, runtime)

    async def hotel_room_info_async(
        self,
        request: btrip_open_20220520_models.HotelRoomInfoRequest,
    ) -> btrip_open_20220520_models.HotelRoomInfoResponse:
        """
        @summary 获取酒店静态房型详情
        
        @param request: HotelRoomInfoRequest
        @return: HotelRoomInfoResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.HotelRoomInfoHeaders()
        return await self.hotel_room_info_with_options_async(request, headers, runtime)

    def hotel_search_with_options(
        self,
        tmp_req: btrip_open_20220520_models.HotelSearchRequest,
        headers: btrip_open_20220520_models.HotelSearchHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.HotelSearchResponse:
        """
        @summary 酒店列表搜索接口(直连)
        
        @param tmp_req: HotelSearchRequest
        @param headers: HotelSearchHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: HotelSearchResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.HotelSearchShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.brand_code):
            request.brand_code_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.brand_code, 'brand_code', 'json')
        if not UtilClient.is_unset(tmp_req.shids):
            request.shids_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.shids, 'shids', 'json')
        query = {}
        if not UtilClient.is_unset(request.adult_num):
            query['adult_num'] = request.adult_num
        if not UtilClient.is_unset(request.brand_code_shrink):
            query['brand_code'] = request.brand_code_shrink
        if not UtilClient.is_unset(request.btrip_user_id):
            query['btrip_user_id'] = request.btrip_user_id
        if not UtilClient.is_unset(request.check_in_date):
            query['check_in_date'] = request.check_in_date
        if not UtilClient.is_unset(request.check_out_date):
            query['check_out_date'] = request.check_out_date
        if not UtilClient.is_unset(request.city_code):
            query['city_code'] = request.city_code
        if not UtilClient.is_unset(request.dir):
            query['dir'] = request.dir
        if not UtilClient.is_unset(request.distance):
            query['distance'] = request.distance
        if not UtilClient.is_unset(request.district_code):
            query['district_code'] = request.district_code
        if not UtilClient.is_unset(request.hotel_star):
            query['hotel_star'] = request.hotel_star
        if not UtilClient.is_unset(request.is_protocol):
            query['is_protocol'] = request.is_protocol
        if not UtilClient.is_unset(request.key_words):
            query['key_words'] = request.key_words
        if not UtilClient.is_unset(request.location):
            query['location'] = request.location
        if not UtilClient.is_unset(request.max_price):
            query['max_price'] = request.max_price
        if not UtilClient.is_unset(request.min_price):
            query['min_price'] = request.min_price
        if not UtilClient.is_unset(request.page_no):
            query['page_no'] = request.page_no
        if not UtilClient.is_unset(request.page_size):
            query['page_size'] = request.page_size
        if not UtilClient.is_unset(request.pay_over_type):
            query['pay_over_type'] = request.pay_over_type
        if not UtilClient.is_unset(request.payment_type):
            query['payment_type'] = request.payment_type
        if not UtilClient.is_unset(request.shids_shrink):
            query['shids'] = request.shids_shrink
        if not UtilClient.is_unset(request.sort_code):
            query['sort_code'] = request.sort_code
        if not UtilClient.is_unset(request.super_man):
            query['super_man'] = request.super_man
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='HotelSearch',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-hotel/v1/hotels/action/search',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.HotelSearchResponse(),
            self.call_api(params, req, runtime)
        )

    async def hotel_search_with_options_async(
        self,
        tmp_req: btrip_open_20220520_models.HotelSearchRequest,
        headers: btrip_open_20220520_models.HotelSearchHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.HotelSearchResponse:
        """
        @summary 酒店列表搜索接口(直连)
        
        @param tmp_req: HotelSearchRequest
        @param headers: HotelSearchHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: HotelSearchResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.HotelSearchShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.brand_code):
            request.brand_code_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.brand_code, 'brand_code', 'json')
        if not UtilClient.is_unset(tmp_req.shids):
            request.shids_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.shids, 'shids', 'json')
        query = {}
        if not UtilClient.is_unset(request.adult_num):
            query['adult_num'] = request.adult_num
        if not UtilClient.is_unset(request.brand_code_shrink):
            query['brand_code'] = request.brand_code_shrink
        if not UtilClient.is_unset(request.btrip_user_id):
            query['btrip_user_id'] = request.btrip_user_id
        if not UtilClient.is_unset(request.check_in_date):
            query['check_in_date'] = request.check_in_date
        if not UtilClient.is_unset(request.check_out_date):
            query['check_out_date'] = request.check_out_date
        if not UtilClient.is_unset(request.city_code):
            query['city_code'] = request.city_code
        if not UtilClient.is_unset(request.dir):
            query['dir'] = request.dir
        if not UtilClient.is_unset(request.distance):
            query['distance'] = request.distance
        if not UtilClient.is_unset(request.district_code):
            query['district_code'] = request.district_code
        if not UtilClient.is_unset(request.hotel_star):
            query['hotel_star'] = request.hotel_star
        if not UtilClient.is_unset(request.is_protocol):
            query['is_protocol'] = request.is_protocol
        if not UtilClient.is_unset(request.key_words):
            query['key_words'] = request.key_words
        if not UtilClient.is_unset(request.location):
            query['location'] = request.location
        if not UtilClient.is_unset(request.max_price):
            query['max_price'] = request.max_price
        if not UtilClient.is_unset(request.min_price):
            query['min_price'] = request.min_price
        if not UtilClient.is_unset(request.page_no):
            query['page_no'] = request.page_no
        if not UtilClient.is_unset(request.page_size):
            query['page_size'] = request.page_size
        if not UtilClient.is_unset(request.pay_over_type):
            query['pay_over_type'] = request.pay_over_type
        if not UtilClient.is_unset(request.payment_type):
            query['payment_type'] = request.payment_type
        if not UtilClient.is_unset(request.shids_shrink):
            query['shids'] = request.shids_shrink
        if not UtilClient.is_unset(request.sort_code):
            query['sort_code'] = request.sort_code
        if not UtilClient.is_unset(request.super_man):
            query['super_man'] = request.super_man
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='HotelSearch',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-hotel/v1/hotels/action/search',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.HotelSearchResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def hotel_search(
        self,
        request: btrip_open_20220520_models.HotelSearchRequest,
    ) -> btrip_open_20220520_models.HotelSearchResponse:
        """
        @summary 酒店列表搜索接口(直连)
        
        @param request: HotelSearchRequest
        @return: HotelSearchResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.HotelSearchHeaders()
        return self.hotel_search_with_options(request, headers, runtime)

    async def hotel_search_async(
        self,
        request: btrip_open_20220520_models.HotelSearchRequest,
    ) -> btrip_open_20220520_models.HotelSearchResponse:
        """
        @summary 酒店列表搜索接口(直连)
        
        @param request: HotelSearchRequest
        @return: HotelSearchResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.HotelSearchHeaders()
        return await self.hotel_search_with_options_async(request, headers, runtime)

    def hotel_static_info_with_options(
        self,
        tmp_req: btrip_open_20220520_models.HotelStaticInfoRequest,
        headers: btrip_open_20220520_models.HotelStaticInfoHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.HotelStaticInfoResponse:
        """
        @summary 查询酒店静态详情
        
        @param tmp_req: HotelStaticInfoRequest
        @param headers: HotelStaticInfoHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: HotelStaticInfoResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.HotelStaticInfoShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.hotel_ids):
            request.hotel_ids_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.hotel_ids, 'hotel_ids', 'json')
        query = {}
        if not UtilClient.is_unset(request.hotel_ids_shrink):
            query['hotel_ids'] = request.hotel_ids_shrink
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='HotelStaticInfo',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-hotel/v1/static-infos',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.HotelStaticInfoResponse(),
            self.call_api(params, req, runtime)
        )

    async def hotel_static_info_with_options_async(
        self,
        tmp_req: btrip_open_20220520_models.HotelStaticInfoRequest,
        headers: btrip_open_20220520_models.HotelStaticInfoHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.HotelStaticInfoResponse:
        """
        @summary 查询酒店静态详情
        
        @param tmp_req: HotelStaticInfoRequest
        @param headers: HotelStaticInfoHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: HotelStaticInfoResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.HotelStaticInfoShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.hotel_ids):
            request.hotel_ids_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.hotel_ids, 'hotel_ids', 'json')
        query = {}
        if not UtilClient.is_unset(request.hotel_ids_shrink):
            query['hotel_ids'] = request.hotel_ids_shrink
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='HotelStaticInfo',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-hotel/v1/static-infos',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.HotelStaticInfoResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def hotel_static_info(
        self,
        request: btrip_open_20220520_models.HotelStaticInfoRequest,
    ) -> btrip_open_20220520_models.HotelStaticInfoResponse:
        """
        @summary 查询酒店静态详情
        
        @param request: HotelStaticInfoRequest
        @return: HotelStaticInfoResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.HotelStaticInfoHeaders()
        return self.hotel_static_info_with_options(request, headers, runtime)

    async def hotel_static_info_async(
        self,
        request: btrip_open_20220520_models.HotelStaticInfoRequest,
    ) -> btrip_open_20220520_models.HotelStaticInfoResponse:
        """
        @summary 查询酒店静态详情
        
        @param request: HotelStaticInfoRequest
        @return: HotelStaticInfoResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.HotelStaticInfoHeaders()
        return await self.hotel_static_info_with_options_async(request, headers, runtime)

    def ie_flight_bill_settlement_query_with_options(
        self,
        request: btrip_open_20220520_models.IeFlightBillSettlementQueryRequest,
        headers: btrip_open_20220520_models.IeFlightBillSettlementQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.IeFlightBillSettlementQueryResponse:
        """
        @summary 查询国际机票记账数据
        
        @param request: IeFlightBillSettlementQueryRequest
        @param headers: IeFlightBillSettlementQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: IeFlightBillSettlementQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.page_no):
            query['page_no'] = request.page_no
        if not UtilClient.is_unset(request.page_size):
            query['page_size'] = request.page_size
        if not UtilClient.is_unset(request.period_end):
            query['period_end'] = request.period_end
        if not UtilClient.is_unset(request.period_start):
            query['period_start'] = request.period_start
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='IeFlightBillSettlementQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/ie-flight/v1/bill-settlement',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.IeFlightBillSettlementQueryResponse(),
            self.call_api(params, req, runtime)
        )

    async def ie_flight_bill_settlement_query_with_options_async(
        self,
        request: btrip_open_20220520_models.IeFlightBillSettlementQueryRequest,
        headers: btrip_open_20220520_models.IeFlightBillSettlementQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.IeFlightBillSettlementQueryResponse:
        """
        @summary 查询国际机票记账数据
        
        @param request: IeFlightBillSettlementQueryRequest
        @param headers: IeFlightBillSettlementQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: IeFlightBillSettlementQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.page_no):
            query['page_no'] = request.page_no
        if not UtilClient.is_unset(request.page_size):
            query['page_size'] = request.page_size
        if not UtilClient.is_unset(request.period_end):
            query['period_end'] = request.period_end
        if not UtilClient.is_unset(request.period_start):
            query['period_start'] = request.period_start
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='IeFlightBillSettlementQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/ie-flight/v1/bill-settlement',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.IeFlightBillSettlementQueryResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def ie_flight_bill_settlement_query(
        self,
        request: btrip_open_20220520_models.IeFlightBillSettlementQueryRequest,
    ) -> btrip_open_20220520_models.IeFlightBillSettlementQueryResponse:
        """
        @summary 查询国际机票记账数据
        
        @param request: IeFlightBillSettlementQueryRequest
        @return: IeFlightBillSettlementQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.IeFlightBillSettlementQueryHeaders()
        return self.ie_flight_bill_settlement_query_with_options(request, headers, runtime)

    async def ie_flight_bill_settlement_query_async(
        self,
        request: btrip_open_20220520_models.IeFlightBillSettlementQueryRequest,
    ) -> btrip_open_20220520_models.IeFlightBillSettlementQueryResponse:
        """
        @summary 查询国际机票记账数据
        
        @param request: IeFlightBillSettlementQueryRequest
        @return: IeFlightBillSettlementQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.IeFlightBillSettlementQueryHeaders()
        return await self.ie_flight_bill_settlement_query_with_options_async(request, headers, runtime)

    def ie_hotel_bill_settlement_query_with_options(
        self,
        request: btrip_open_20220520_models.IeHotelBillSettlementQueryRequest,
        headers: btrip_open_20220520_models.IeHotelBillSettlementQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.IeHotelBillSettlementQueryResponse:
        """
        @summary 查询国际/中国港澳台酒店记账数据
        
        @param request: IeHotelBillSettlementQueryRequest
        @param headers: IeHotelBillSettlementQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: IeHotelBillSettlementQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.category):
            query['category'] = request.category
        if not UtilClient.is_unset(request.page_no):
            query['page_no'] = request.page_no
        if not UtilClient.is_unset(request.page_size):
            query['page_size'] = request.page_size
        if not UtilClient.is_unset(request.period_end):
            query['period_end'] = request.period_end
        if not UtilClient.is_unset(request.period_start):
            query['period_start'] = request.period_start
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='IeHotelBillSettlementQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/ie-hotel/v1/bill-settlement',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.IeHotelBillSettlementQueryResponse(),
            self.call_api(params, req, runtime)
        )

    async def ie_hotel_bill_settlement_query_with_options_async(
        self,
        request: btrip_open_20220520_models.IeHotelBillSettlementQueryRequest,
        headers: btrip_open_20220520_models.IeHotelBillSettlementQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.IeHotelBillSettlementQueryResponse:
        """
        @summary 查询国际/中国港澳台酒店记账数据
        
        @param request: IeHotelBillSettlementQueryRequest
        @param headers: IeHotelBillSettlementQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: IeHotelBillSettlementQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.category):
            query['category'] = request.category
        if not UtilClient.is_unset(request.page_no):
            query['page_no'] = request.page_no
        if not UtilClient.is_unset(request.page_size):
            query['page_size'] = request.page_size
        if not UtilClient.is_unset(request.period_end):
            query['period_end'] = request.period_end
        if not UtilClient.is_unset(request.period_start):
            query['period_start'] = request.period_start
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='IeHotelBillSettlementQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/ie-hotel/v1/bill-settlement',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.IeHotelBillSettlementQueryResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def ie_hotel_bill_settlement_query(
        self,
        request: btrip_open_20220520_models.IeHotelBillSettlementQueryRequest,
    ) -> btrip_open_20220520_models.IeHotelBillSettlementQueryResponse:
        """
        @summary 查询国际/中国港澳台酒店记账数据
        
        @param request: IeHotelBillSettlementQueryRequest
        @return: IeHotelBillSettlementQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.IeHotelBillSettlementQueryHeaders()
        return self.ie_hotel_bill_settlement_query_with_options(request, headers, runtime)

    async def ie_hotel_bill_settlement_query_async(
        self,
        request: btrip_open_20220520_models.IeHotelBillSettlementQueryRequest,
    ) -> btrip_open_20220520_models.IeHotelBillSettlementQueryResponse:
        """
        @summary 查询国际/中国港澳台酒店记账数据
        
        @param request: IeHotelBillSettlementQueryRequest
        @return: IeHotelBillSettlementQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.IeHotelBillSettlementQueryHeaders()
        return await self.ie_hotel_bill_settlement_query_with_options_async(request, headers, runtime)

    def ins_invoice_scan_query_with_options(
        self,
        request: btrip_open_20220520_models.InsInvoiceScanQueryRequest,
        headers: btrip_open_20220520_models.InsInvoiceScanQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.InsInvoiceScanQueryResponse:
        """
        @summary 查询保险电子发票
        
        @param request: InsInvoiceScanQueryRequest
        @param headers: InsInvoiceScanQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: InsInvoiceScanQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.bill_date):
            query['bill_date'] = request.bill_date
        if not UtilClient.is_unset(request.bill_id):
            query['bill_id'] = request.bill_id
        if not UtilClient.is_unset(request.invoice_sub_task_id):
            query['invoice_sub_task_id'] = request.invoice_sub_task_id
        if not UtilClient.is_unset(request.page_no):
            query['page_no'] = request.page_no
        if not UtilClient.is_unset(request.page_size):
            query['page_size'] = request.page_size
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='InsInvoiceScanQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/scan/v1/ins-invoice',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.InsInvoiceScanQueryResponse(),
            self.call_api(params, req, runtime)
        )

    async def ins_invoice_scan_query_with_options_async(
        self,
        request: btrip_open_20220520_models.InsInvoiceScanQueryRequest,
        headers: btrip_open_20220520_models.InsInvoiceScanQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.InsInvoiceScanQueryResponse:
        """
        @summary 查询保险电子发票
        
        @param request: InsInvoiceScanQueryRequest
        @param headers: InsInvoiceScanQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: InsInvoiceScanQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.bill_date):
            query['bill_date'] = request.bill_date
        if not UtilClient.is_unset(request.bill_id):
            query['bill_id'] = request.bill_id
        if not UtilClient.is_unset(request.invoice_sub_task_id):
            query['invoice_sub_task_id'] = request.invoice_sub_task_id
        if not UtilClient.is_unset(request.page_no):
            query['page_no'] = request.page_no
        if not UtilClient.is_unset(request.page_size):
            query['page_size'] = request.page_size
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='InsInvoiceScanQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/scan/v1/ins-invoice',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.InsInvoiceScanQueryResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def ins_invoice_scan_query(
        self,
        request: btrip_open_20220520_models.InsInvoiceScanQueryRequest,
    ) -> btrip_open_20220520_models.InsInvoiceScanQueryResponse:
        """
        @summary 查询保险电子发票
        
        @param request: InsInvoiceScanQueryRequest
        @return: InsInvoiceScanQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.InsInvoiceScanQueryHeaders()
        return self.ins_invoice_scan_query_with_options(request, headers, runtime)

    async def ins_invoice_scan_query_async(
        self,
        request: btrip_open_20220520_models.InsInvoiceScanQueryRequest,
    ) -> btrip_open_20220520_models.InsInvoiceScanQueryResponse:
        """
        @summary 查询保险电子发票
        
        @param request: InsInvoiceScanQueryRequest
        @return: InsInvoiceScanQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.InsInvoiceScanQueryHeaders()
        return await self.ins_invoice_scan_query_with_options_async(request, headers, runtime)

    def insure_order_apply_with_options(
        self,
        request: btrip_open_20220520_models.InsureOrderApplyRequest,
        headers: btrip_open_20220520_models.InsureOrderApplyHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.InsureOrderApplyResponse:
        """
        @summary 保险订单申请
        
        @param request: InsureOrderApplyRequest
        @param headers: InsureOrderApplyHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: InsureOrderApplyResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.btrip_user_id):
            body['btrip_user_id'] = request.btrip_user_id
        if not UtilClient.is_unset(request.buyer_name):
            body['buyer_name'] = request.buyer_name
        if not UtilClient.is_unset(request.ins_order_id):
            body['ins_order_id'] = request.ins_order_id
        if not UtilClient.is_unset(request.isv_name):
            body['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.out_order_id):
            body['out_order_id'] = request.out_order_id
        if not UtilClient.is_unset(request.out_sub_order_id):
            body['out_sub_order_id'] = request.out_sub_order_id
        if not UtilClient.is_unset(request.supplier_code):
            body['supplier_code'] = request.supplier_code
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='InsureOrderApply',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v1/insurances/action/apply',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.InsureOrderApplyResponse(),
            self.call_api(params, req, runtime)
        )

    async def insure_order_apply_with_options_async(
        self,
        request: btrip_open_20220520_models.InsureOrderApplyRequest,
        headers: btrip_open_20220520_models.InsureOrderApplyHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.InsureOrderApplyResponse:
        """
        @summary 保险订单申请
        
        @param request: InsureOrderApplyRequest
        @param headers: InsureOrderApplyHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: InsureOrderApplyResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.btrip_user_id):
            body['btrip_user_id'] = request.btrip_user_id
        if not UtilClient.is_unset(request.buyer_name):
            body['buyer_name'] = request.buyer_name
        if not UtilClient.is_unset(request.ins_order_id):
            body['ins_order_id'] = request.ins_order_id
        if not UtilClient.is_unset(request.isv_name):
            body['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.out_order_id):
            body['out_order_id'] = request.out_order_id
        if not UtilClient.is_unset(request.out_sub_order_id):
            body['out_sub_order_id'] = request.out_sub_order_id
        if not UtilClient.is_unset(request.supplier_code):
            body['supplier_code'] = request.supplier_code
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='InsureOrderApply',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v1/insurances/action/apply',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.InsureOrderApplyResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def insure_order_apply(
        self,
        request: btrip_open_20220520_models.InsureOrderApplyRequest,
    ) -> btrip_open_20220520_models.InsureOrderApplyResponse:
        """
        @summary 保险订单申请
        
        @param request: InsureOrderApplyRequest
        @return: InsureOrderApplyResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.InsureOrderApplyHeaders()
        return self.insure_order_apply_with_options(request, headers, runtime)

    async def insure_order_apply_async(
        self,
        request: btrip_open_20220520_models.InsureOrderApplyRequest,
    ) -> btrip_open_20220520_models.InsureOrderApplyResponse:
        """
        @summary 保险订单申请
        
        @param request: InsureOrderApplyRequest
        @return: InsureOrderApplyResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.InsureOrderApplyHeaders()
        return await self.insure_order_apply_with_options_async(request, headers, runtime)

    def insure_order_cancel_with_options(
        self,
        ins_order_id: str,
        request: btrip_open_20220520_models.InsureOrderCancelRequest,
        headers: btrip_open_20220520_models.InsureOrderCancelHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.InsureOrderCancelResponse:
        """
        @summary 保险订单取消
        
        @param request: InsureOrderCancelRequest
        @param headers: InsureOrderCancelHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: InsureOrderCancelResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.btrip_user_id):
            query['btrip_user_id'] = request.btrip_user_id
        if not UtilClient.is_unset(request.buyer_name):
            query['buyer_name'] = request.buyer_name
        if not UtilClient.is_unset(request.isv_name):
            query['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.supplier_code):
            query['supplier_code'] = request.supplier_code
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='InsureOrderCancel',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v1/insurances/{OpenApiUtilClient.get_encode_param(ins_order_id)}/action/cancel',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.InsureOrderCancelResponse(),
            self.call_api(params, req, runtime)
        )

    async def insure_order_cancel_with_options_async(
        self,
        ins_order_id: str,
        request: btrip_open_20220520_models.InsureOrderCancelRequest,
        headers: btrip_open_20220520_models.InsureOrderCancelHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.InsureOrderCancelResponse:
        """
        @summary 保险订单取消
        
        @param request: InsureOrderCancelRequest
        @param headers: InsureOrderCancelHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: InsureOrderCancelResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.btrip_user_id):
            query['btrip_user_id'] = request.btrip_user_id
        if not UtilClient.is_unset(request.buyer_name):
            query['buyer_name'] = request.buyer_name
        if not UtilClient.is_unset(request.isv_name):
            query['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.supplier_code):
            query['supplier_code'] = request.supplier_code
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='InsureOrderCancel',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v1/insurances/{OpenApiUtilClient.get_encode_param(ins_order_id)}/action/cancel',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.InsureOrderCancelResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def insure_order_cancel(
        self,
        ins_order_id: str,
        request: btrip_open_20220520_models.InsureOrderCancelRequest,
    ) -> btrip_open_20220520_models.InsureOrderCancelResponse:
        """
        @summary 保险订单取消
        
        @param request: InsureOrderCancelRequest
        @return: InsureOrderCancelResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.InsureOrderCancelHeaders()
        return self.insure_order_cancel_with_options(ins_order_id, request, headers, runtime)

    async def insure_order_cancel_async(
        self,
        ins_order_id: str,
        request: btrip_open_20220520_models.InsureOrderCancelRequest,
    ) -> btrip_open_20220520_models.InsureOrderCancelResponse:
        """
        @summary 保险订单取消
        
        @param request: InsureOrderCancelRequest
        @return: InsureOrderCancelResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.InsureOrderCancelHeaders()
        return await self.insure_order_cancel_with_options_async(ins_order_id, request, headers, runtime)

    def insure_order_create_with_options(
        self,
        tmp_req: btrip_open_20220520_models.InsureOrderCreateRequest,
        headers: btrip_open_20220520_models.InsureOrderCreateHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.InsureOrderCreateResponse:
        """
        @summary 保险订单创建
        
        @param tmp_req: InsureOrderCreateRequest
        @param headers: InsureOrderCreateHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: InsureOrderCreateResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.InsureOrderCreateShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.applicant):
            request.applicant_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.applicant, 'applicant', 'json')
        if not UtilClient.is_unset(tmp_req.ins_person_and_segment_list):
            request.ins_person_and_segment_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.ins_person_and_segment_list, 'ins_person_and_segment_list', 'json')
        body = {}
        if not UtilClient.is_unset(request.applicant_shrink):
            body['applicant'] = request.applicant_shrink
        if not UtilClient.is_unset(request.btrip_user_id):
            body['btrip_user_id'] = request.btrip_user_id
        if not UtilClient.is_unset(request.buyer_name):
            body['buyer_name'] = request.buyer_name
        if not UtilClient.is_unset(request.ins_person_and_segment_list_shrink):
            body['ins_person_and_segment_list'] = request.ins_person_and_segment_list_shrink
        if not UtilClient.is_unset(request.isv_name):
            body['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.out_ins_order_id):
            body['out_ins_order_id'] = request.out_ins_order_id
        if not UtilClient.is_unset(request.out_order_id):
            body['out_order_id'] = request.out_order_id
        if not UtilClient.is_unset(request.out_sub_order_id):
            body['out_sub_order_id'] = request.out_sub_order_id
        if not UtilClient.is_unset(request.supplier_code):
            body['supplier_code'] = request.supplier_code
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='InsureOrderCreate',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v1/insurances/action/create',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.InsureOrderCreateResponse(),
            self.call_api(params, req, runtime)
        )

    async def insure_order_create_with_options_async(
        self,
        tmp_req: btrip_open_20220520_models.InsureOrderCreateRequest,
        headers: btrip_open_20220520_models.InsureOrderCreateHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.InsureOrderCreateResponse:
        """
        @summary 保险订单创建
        
        @param tmp_req: InsureOrderCreateRequest
        @param headers: InsureOrderCreateHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: InsureOrderCreateResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.InsureOrderCreateShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.applicant):
            request.applicant_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.applicant, 'applicant', 'json')
        if not UtilClient.is_unset(tmp_req.ins_person_and_segment_list):
            request.ins_person_and_segment_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.ins_person_and_segment_list, 'ins_person_and_segment_list', 'json')
        body = {}
        if not UtilClient.is_unset(request.applicant_shrink):
            body['applicant'] = request.applicant_shrink
        if not UtilClient.is_unset(request.btrip_user_id):
            body['btrip_user_id'] = request.btrip_user_id
        if not UtilClient.is_unset(request.buyer_name):
            body['buyer_name'] = request.buyer_name
        if not UtilClient.is_unset(request.ins_person_and_segment_list_shrink):
            body['ins_person_and_segment_list'] = request.ins_person_and_segment_list_shrink
        if not UtilClient.is_unset(request.isv_name):
            body['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.out_ins_order_id):
            body['out_ins_order_id'] = request.out_ins_order_id
        if not UtilClient.is_unset(request.out_order_id):
            body['out_order_id'] = request.out_order_id
        if not UtilClient.is_unset(request.out_sub_order_id):
            body['out_sub_order_id'] = request.out_sub_order_id
        if not UtilClient.is_unset(request.supplier_code):
            body['supplier_code'] = request.supplier_code
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='InsureOrderCreate',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v1/insurances/action/create',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.InsureOrderCreateResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def insure_order_create(
        self,
        request: btrip_open_20220520_models.InsureOrderCreateRequest,
    ) -> btrip_open_20220520_models.InsureOrderCreateResponse:
        """
        @summary 保险订单创建
        
        @param request: InsureOrderCreateRequest
        @return: InsureOrderCreateResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.InsureOrderCreateHeaders()
        return self.insure_order_create_with_options(request, headers, runtime)

    async def insure_order_create_async(
        self,
        request: btrip_open_20220520_models.InsureOrderCreateRequest,
    ) -> btrip_open_20220520_models.InsureOrderCreateResponse:
        """
        @summary 保险订单创建
        
        @param request: InsureOrderCreateRequest
        @return: InsureOrderCreateResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.InsureOrderCreateHeaders()
        return await self.insure_order_create_with_options_async(request, headers, runtime)

    def insure_order_detail_with_options(
        self,
        request: btrip_open_20220520_models.InsureOrderDetailRequest,
        headers: btrip_open_20220520_models.InsureOrderDetailHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.InsureOrderDetailResponse:
        """
        @summary 保险订单查询
        
        @param request: InsureOrderDetailRequest
        @param headers: InsureOrderDetailHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: InsureOrderDetailResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.btrip_user_id):
            query['btrip_user_id'] = request.btrip_user_id
        if not UtilClient.is_unset(request.buyer_name):
            query['buyer_name'] = request.buyer_name
        if not UtilClient.is_unset(request.ins_order_id):
            query['ins_order_id'] = request.ins_order_id
        if not UtilClient.is_unset(request.isv_name):
            query['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.supplier_code):
            query['supplier_code'] = request.supplier_code
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='InsureOrderDetail',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v1/insurances/action/detail',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.InsureOrderDetailResponse(),
            self.call_api(params, req, runtime)
        )

    async def insure_order_detail_with_options_async(
        self,
        request: btrip_open_20220520_models.InsureOrderDetailRequest,
        headers: btrip_open_20220520_models.InsureOrderDetailHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.InsureOrderDetailResponse:
        """
        @summary 保险订单查询
        
        @param request: InsureOrderDetailRequest
        @param headers: InsureOrderDetailHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: InsureOrderDetailResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.btrip_user_id):
            query['btrip_user_id'] = request.btrip_user_id
        if not UtilClient.is_unset(request.buyer_name):
            query['buyer_name'] = request.buyer_name
        if not UtilClient.is_unset(request.ins_order_id):
            query['ins_order_id'] = request.ins_order_id
        if not UtilClient.is_unset(request.isv_name):
            query['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.supplier_code):
            query['supplier_code'] = request.supplier_code
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='InsureOrderDetail',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v1/insurances/action/detail',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.InsureOrderDetailResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def insure_order_detail(
        self,
        request: btrip_open_20220520_models.InsureOrderDetailRequest,
    ) -> btrip_open_20220520_models.InsureOrderDetailResponse:
        """
        @summary 保险订单查询
        
        @param request: InsureOrderDetailRequest
        @return: InsureOrderDetailResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.InsureOrderDetailHeaders()
        return self.insure_order_detail_with_options(request, headers, runtime)

    async def insure_order_detail_async(
        self,
        request: btrip_open_20220520_models.InsureOrderDetailRequest,
    ) -> btrip_open_20220520_models.InsureOrderDetailResponse:
        """
        @summary 保险订单查询
        
        @param request: InsureOrderDetailRequest
        @return: InsureOrderDetailResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.InsureOrderDetailHeaders()
        return await self.insure_order_detail_with_options_async(request, headers, runtime)

    def insure_order_pay_with_options(
        self,
        ins_order_id: str,
        request: btrip_open_20220520_models.InsureOrderPayRequest,
        headers: btrip_open_20220520_models.InsureOrderPayHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.InsureOrderPayResponse:
        """
        @summary 保险订单支付
        
        @param request: InsureOrderPayRequest
        @param headers: InsureOrderPayHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: InsureOrderPayResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.btrip_user_id):
            body['btrip_user_id'] = request.btrip_user_id
        if not UtilClient.is_unset(request.buyer_name):
            body['buyer_name'] = request.buyer_name
        if not UtilClient.is_unset(request.isv_name):
            body['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.out_order_id):
            body['out_order_id'] = request.out_order_id
        if not UtilClient.is_unset(request.out_sub_order_id):
            body['out_sub_order_id'] = request.out_sub_order_id
        if not UtilClient.is_unset(request.payment_amount):
            body['payment_amount'] = request.payment_amount
        if not UtilClient.is_unset(request.supplier_code):
            body['supplier_code'] = request.supplier_code
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='InsureOrderPay',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v1/insurances/{OpenApiUtilClient.get_encode_param(ins_order_id)}/action/pay',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.InsureOrderPayResponse(),
            self.call_api(params, req, runtime)
        )

    async def insure_order_pay_with_options_async(
        self,
        ins_order_id: str,
        request: btrip_open_20220520_models.InsureOrderPayRequest,
        headers: btrip_open_20220520_models.InsureOrderPayHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.InsureOrderPayResponse:
        """
        @summary 保险订单支付
        
        @param request: InsureOrderPayRequest
        @param headers: InsureOrderPayHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: InsureOrderPayResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.btrip_user_id):
            body['btrip_user_id'] = request.btrip_user_id
        if not UtilClient.is_unset(request.buyer_name):
            body['buyer_name'] = request.buyer_name
        if not UtilClient.is_unset(request.isv_name):
            body['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.out_order_id):
            body['out_order_id'] = request.out_order_id
        if not UtilClient.is_unset(request.out_sub_order_id):
            body['out_sub_order_id'] = request.out_sub_order_id
        if not UtilClient.is_unset(request.payment_amount):
            body['payment_amount'] = request.payment_amount
        if not UtilClient.is_unset(request.supplier_code):
            body['supplier_code'] = request.supplier_code
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='InsureOrderPay',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v1/insurances/{OpenApiUtilClient.get_encode_param(ins_order_id)}/action/pay',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.InsureOrderPayResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def insure_order_pay(
        self,
        ins_order_id: str,
        request: btrip_open_20220520_models.InsureOrderPayRequest,
    ) -> btrip_open_20220520_models.InsureOrderPayResponse:
        """
        @summary 保险订单支付
        
        @param request: InsureOrderPayRequest
        @return: InsureOrderPayResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.InsureOrderPayHeaders()
        return self.insure_order_pay_with_options(ins_order_id, request, headers, runtime)

    async def insure_order_pay_async(
        self,
        ins_order_id: str,
        request: btrip_open_20220520_models.InsureOrderPayRequest,
    ) -> btrip_open_20220520_models.InsureOrderPayResponse:
        """
        @summary 保险订单支付
        
        @param request: InsureOrderPayRequest
        @return: InsureOrderPayResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.InsureOrderPayHeaders()
        return await self.insure_order_pay_with_options_async(ins_order_id, request, headers, runtime)

    def insure_order_refund_with_options(
        self,
        ins_order_id: str,
        tmp_req: btrip_open_20220520_models.InsureOrderRefundRequest,
        headers: btrip_open_20220520_models.InsureOrderRefundHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.InsureOrderRefundResponse:
        """
        @summary 保险订单退保
        
        @param tmp_req: InsureOrderRefundRequest
        @param headers: InsureOrderRefundHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: InsureOrderRefundResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.InsureOrderRefundShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.policy_no_list):
            request.policy_no_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.policy_no_list, 'policy_no_list', 'json')
        if not UtilClient.is_unset(tmp_req.sub_ins_order_ids):
            request.sub_ins_order_ids_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.sub_ins_order_ids, 'sub_ins_order_ids', 'json')
        body = {}
        if not UtilClient.is_unset(request.btrip_user_id):
            body['btrip_user_id'] = request.btrip_user_id
        if not UtilClient.is_unset(request.buyer_name):
            body['buyer_name'] = request.buyer_name
        if not UtilClient.is_unset(request.isv_name):
            body['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.out_apply_id):
            body['out_apply_id'] = request.out_apply_id
        if not UtilClient.is_unset(request.policy_no_list_shrink):
            body['policy_no_list'] = request.policy_no_list_shrink
        if not UtilClient.is_unset(request.sub_ins_order_ids_shrink):
            body['sub_ins_order_ids'] = request.sub_ins_order_ids_shrink
        if not UtilClient.is_unset(request.supplier_code):
            body['supplier_code'] = request.supplier_code
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='InsureOrderRefund',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v1/insurances/{OpenApiUtilClient.get_encode_param(ins_order_id)}/action/refund',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.InsureOrderRefundResponse(),
            self.call_api(params, req, runtime)
        )

    async def insure_order_refund_with_options_async(
        self,
        ins_order_id: str,
        tmp_req: btrip_open_20220520_models.InsureOrderRefundRequest,
        headers: btrip_open_20220520_models.InsureOrderRefundHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.InsureOrderRefundResponse:
        """
        @summary 保险订单退保
        
        @param tmp_req: InsureOrderRefundRequest
        @param headers: InsureOrderRefundHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: InsureOrderRefundResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.InsureOrderRefundShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.policy_no_list):
            request.policy_no_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.policy_no_list, 'policy_no_list', 'json')
        if not UtilClient.is_unset(tmp_req.sub_ins_order_ids):
            request.sub_ins_order_ids_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.sub_ins_order_ids, 'sub_ins_order_ids', 'json')
        body = {}
        if not UtilClient.is_unset(request.btrip_user_id):
            body['btrip_user_id'] = request.btrip_user_id
        if not UtilClient.is_unset(request.buyer_name):
            body['buyer_name'] = request.buyer_name
        if not UtilClient.is_unset(request.isv_name):
            body['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.out_apply_id):
            body['out_apply_id'] = request.out_apply_id
        if not UtilClient.is_unset(request.policy_no_list_shrink):
            body['policy_no_list'] = request.policy_no_list_shrink
        if not UtilClient.is_unset(request.sub_ins_order_ids_shrink):
            body['sub_ins_order_ids'] = request.sub_ins_order_ids_shrink
        if not UtilClient.is_unset(request.supplier_code):
            body['supplier_code'] = request.supplier_code
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='InsureOrderRefund',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v1/insurances/{OpenApiUtilClient.get_encode_param(ins_order_id)}/action/refund',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.InsureOrderRefundResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def insure_order_refund(
        self,
        ins_order_id: str,
        request: btrip_open_20220520_models.InsureOrderRefundRequest,
    ) -> btrip_open_20220520_models.InsureOrderRefundResponse:
        """
        @summary 保险订单退保
        
        @param request: InsureOrderRefundRequest
        @return: InsureOrderRefundResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.InsureOrderRefundHeaders()
        return self.insure_order_refund_with_options(ins_order_id, request, headers, runtime)

    async def insure_order_refund_async(
        self,
        ins_order_id: str,
        request: btrip_open_20220520_models.InsureOrderRefundRequest,
    ) -> btrip_open_20220520_models.InsureOrderRefundResponse:
        """
        @summary 保险订单退保
        
        @param request: InsureOrderRefundRequest
        @return: InsureOrderRefundResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.InsureOrderRefundHeaders()
        return await self.insure_order_refund_with_options_async(ins_order_id, request, headers, runtime)

    def insure_order_url_detail_with_options(
        self,
        ins_order_id: str,
        headers: btrip_open_20220520_models.InsureOrderUrlDetailHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.InsureOrderUrlDetailResponse:
        """
        @summary 查询保单详情链接
        
        @param headers: InsureOrderUrlDetailHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: InsureOrderUrlDetailResponse
        """
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers
        )
        params = open_api_models.Params(
            action='InsureOrderUrlDetail',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v1/insurances/{OpenApiUtilClient.get_encode_param(ins_order_id)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.InsureOrderUrlDetailResponse(),
            self.call_api(params, req, runtime)
        )

    async def insure_order_url_detail_with_options_async(
        self,
        ins_order_id: str,
        headers: btrip_open_20220520_models.InsureOrderUrlDetailHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.InsureOrderUrlDetailResponse:
        """
        @summary 查询保单详情链接
        
        @param headers: InsureOrderUrlDetailHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: InsureOrderUrlDetailResponse
        """
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers
        )
        params = open_api_models.Params(
            action='InsureOrderUrlDetail',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v1/insurances/{OpenApiUtilClient.get_encode_param(ins_order_id)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.InsureOrderUrlDetailResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def insure_order_url_detail(
        self,
        ins_order_id: str,
    ) -> btrip_open_20220520_models.InsureOrderUrlDetailResponse:
        """
        @summary 查询保单详情链接
        
        @return: InsureOrderUrlDetailResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.InsureOrderUrlDetailHeaders()
        return self.insure_order_url_detail_with_options(ins_order_id, headers, runtime)

    async def insure_order_url_detail_async(
        self,
        ins_order_id: str,
    ) -> btrip_open_20220520_models.InsureOrderUrlDetailResponse:
        """
        @summary 查询保单详情链接
        
        @return: InsureOrderUrlDetailResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.InsureOrderUrlDetailHeaders()
        return await self.insure_order_url_detail_with_options_async(ins_order_id, headers, runtime)

    def insure_refund_detail_with_options(
        self,
        request: btrip_open_20220520_models.InsureRefundDetailRequest,
        headers: btrip_open_20220520_models.InsureRefundDetailHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.InsureRefundDetailResponse:
        """
        @summary 退保详情查询
        
        @param request: InsureRefundDetailRequest
        @param headers: InsureRefundDetailHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: InsureRefundDetailResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.apply_id):
            query['apply_id'] = request.apply_id
        if not UtilClient.is_unset(request.btrip_user_id):
            query['btrip_user_id'] = request.btrip_user_id
        if not UtilClient.is_unset(request.buyer_name):
            query['buyer_name'] = request.buyer_name
        if not UtilClient.is_unset(request.ins_order_id):
            query['ins_order_id'] = request.ins_order_id
        if not UtilClient.is_unset(request.isv_name):
            query['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.out_apply_id):
            query['out_apply_id'] = request.out_apply_id
        if not UtilClient.is_unset(request.supplier_code):
            query['supplier_code'] = request.supplier_code
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='InsureRefundDetail',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v1/insurances/action/refund-detail',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.InsureRefundDetailResponse(),
            self.call_api(params, req, runtime)
        )

    async def insure_refund_detail_with_options_async(
        self,
        request: btrip_open_20220520_models.InsureRefundDetailRequest,
        headers: btrip_open_20220520_models.InsureRefundDetailHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.InsureRefundDetailResponse:
        """
        @summary 退保详情查询
        
        @param request: InsureRefundDetailRequest
        @param headers: InsureRefundDetailHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: InsureRefundDetailResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.apply_id):
            query['apply_id'] = request.apply_id
        if not UtilClient.is_unset(request.btrip_user_id):
            query['btrip_user_id'] = request.btrip_user_id
        if not UtilClient.is_unset(request.buyer_name):
            query['buyer_name'] = request.buyer_name
        if not UtilClient.is_unset(request.ins_order_id):
            query['ins_order_id'] = request.ins_order_id
        if not UtilClient.is_unset(request.isv_name):
            query['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.out_apply_id):
            query['out_apply_id'] = request.out_apply_id
        if not UtilClient.is_unset(request.supplier_code):
            query['supplier_code'] = request.supplier_code
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='InsureRefundDetail',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v1/insurances/action/refund-detail',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.InsureRefundDetailResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def insure_refund_detail(
        self,
        request: btrip_open_20220520_models.InsureRefundDetailRequest,
    ) -> btrip_open_20220520_models.InsureRefundDetailResponse:
        """
        @summary 退保详情查询
        
        @param request: InsureRefundDetailRequest
        @return: InsureRefundDetailResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.InsureRefundDetailHeaders()
        return self.insure_refund_detail_with_options(request, headers, runtime)

    async def insure_refund_detail_async(
        self,
        request: btrip_open_20220520_models.InsureRefundDetailRequest,
    ) -> btrip_open_20220520_models.InsureRefundDetailResponse:
        """
        @summary 退保详情查询
        
        @param request: InsureRefundDetailRequest
        @return: InsureRefundDetailResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.InsureRefundDetailHeaders()
        return await self.insure_refund_detail_with_options_async(request, headers, runtime)

    def intl_flight_create_order_with_options(
        self,
        tmp_req: btrip_open_20220520_models.IntlFlightCreateOrderRequest,
        headers: btrip_open_20220520_models.IntlFlightCreateOrderHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.IntlFlightCreateOrderResponse:
        """
        @summary 国际机票创建订单
        
        @param tmp_req: IntlFlightCreateOrderRequest
        @param headers: IntlFlightCreateOrderHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: IntlFlightCreateOrderResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.IntlFlightCreateOrderShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.contact_info):
            request.contact_info_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.contact_info, 'contact_info', 'json')
        if not UtilClient.is_unset(tmp_req.cost_center):
            request.cost_center_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.cost_center, 'cost_center', 'json')
        if not UtilClient.is_unset(tmp_req.extra_info):
            request.extra_info_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.extra_info, 'extra_info', 'json')
        if not UtilClient.is_unset(tmp_req.passenger_list):
            request.passenger_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.passenger_list, 'passenger_list', 'json')
        query = {}
        if not UtilClient.is_unset(request.async_create_order_key):
            query['async_create_order_key'] = request.async_create_order_key
        if not UtilClient.is_unset(request.async_create_order_mode):
            query['async_create_order_mode'] = request.async_create_order_mode
        if not UtilClient.is_unset(request.contact_info_shrink):
            query['contact_info'] = request.contact_info_shrink
        if not UtilClient.is_unset(request.cost_center_shrink):
            query['cost_center'] = request.cost_center_shrink
        if not UtilClient.is_unset(request.extra_info_shrink):
            query['extra_info'] = request.extra_info_shrink
        if not UtilClient.is_unset(request.isv_name):
            query['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.language):
            query['language'] = request.language
        if not UtilClient.is_unset(request.ota_item_id):
            query['ota_item_id'] = request.ota_item_id
        if not UtilClient.is_unset(request.out_order_id):
            query['out_order_id'] = request.out_order_id
        if not UtilClient.is_unset(request.passenger_list_shrink):
            query['passenger_list'] = request.passenger_list_shrink
        if not UtilClient.is_unset(request.render_key):
            query['render_key'] = request.render_key
        if not UtilClient.is_unset(request.total_price_cent):
            query['total_price_cent'] = request.total_price_cent
        if not UtilClient.is_unset(request.user_id):
            query['user_id'] = request.user_id
        if not UtilClient.is_unset(request.user_name):
            query['user_name'] = request.user_name
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='IntlFlightCreateOrder',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/intl-flight/v1/order/action/create',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.IntlFlightCreateOrderResponse(),
            self.call_api(params, req, runtime)
        )

    async def intl_flight_create_order_with_options_async(
        self,
        tmp_req: btrip_open_20220520_models.IntlFlightCreateOrderRequest,
        headers: btrip_open_20220520_models.IntlFlightCreateOrderHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.IntlFlightCreateOrderResponse:
        """
        @summary 国际机票创建订单
        
        @param tmp_req: IntlFlightCreateOrderRequest
        @param headers: IntlFlightCreateOrderHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: IntlFlightCreateOrderResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.IntlFlightCreateOrderShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.contact_info):
            request.contact_info_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.contact_info, 'contact_info', 'json')
        if not UtilClient.is_unset(tmp_req.cost_center):
            request.cost_center_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.cost_center, 'cost_center', 'json')
        if not UtilClient.is_unset(tmp_req.extra_info):
            request.extra_info_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.extra_info, 'extra_info', 'json')
        if not UtilClient.is_unset(tmp_req.passenger_list):
            request.passenger_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.passenger_list, 'passenger_list', 'json')
        query = {}
        if not UtilClient.is_unset(request.async_create_order_key):
            query['async_create_order_key'] = request.async_create_order_key
        if not UtilClient.is_unset(request.async_create_order_mode):
            query['async_create_order_mode'] = request.async_create_order_mode
        if not UtilClient.is_unset(request.contact_info_shrink):
            query['contact_info'] = request.contact_info_shrink
        if not UtilClient.is_unset(request.cost_center_shrink):
            query['cost_center'] = request.cost_center_shrink
        if not UtilClient.is_unset(request.extra_info_shrink):
            query['extra_info'] = request.extra_info_shrink
        if not UtilClient.is_unset(request.isv_name):
            query['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.language):
            query['language'] = request.language
        if not UtilClient.is_unset(request.ota_item_id):
            query['ota_item_id'] = request.ota_item_id
        if not UtilClient.is_unset(request.out_order_id):
            query['out_order_id'] = request.out_order_id
        if not UtilClient.is_unset(request.passenger_list_shrink):
            query['passenger_list'] = request.passenger_list_shrink
        if not UtilClient.is_unset(request.render_key):
            query['render_key'] = request.render_key
        if not UtilClient.is_unset(request.total_price_cent):
            query['total_price_cent'] = request.total_price_cent
        if not UtilClient.is_unset(request.user_id):
            query['user_id'] = request.user_id
        if not UtilClient.is_unset(request.user_name):
            query['user_name'] = request.user_name
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='IntlFlightCreateOrder',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/intl-flight/v1/order/action/create',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.IntlFlightCreateOrderResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def intl_flight_create_order(
        self,
        request: btrip_open_20220520_models.IntlFlightCreateOrderRequest,
    ) -> btrip_open_20220520_models.IntlFlightCreateOrderResponse:
        """
        @summary 国际机票创建订单
        
        @param request: IntlFlightCreateOrderRequest
        @return: IntlFlightCreateOrderResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.IntlFlightCreateOrderHeaders()
        return self.intl_flight_create_order_with_options(request, headers, runtime)

    async def intl_flight_create_order_async(
        self,
        request: btrip_open_20220520_models.IntlFlightCreateOrderRequest,
    ) -> btrip_open_20220520_models.IntlFlightCreateOrderResponse:
        """
        @summary 国际机票创建订单
        
        @param request: IntlFlightCreateOrderRequest
        @return: IntlFlightCreateOrderResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.IntlFlightCreateOrderHeaders()
        return await self.intl_flight_create_order_with_options_async(request, headers, runtime)

    def intl_flight_inventory_price_check_with_options(
        self,
        tmp_req: btrip_open_20220520_models.IntlFlightInventoryPriceCheckRequest,
        headers: btrip_open_20220520_models.IntlFlightInventoryPriceCheckHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.IntlFlightInventoryPriceCheckResponse:
        """
        @summary 国际机票验舱验价
        
        @param tmp_req: IntlFlightInventoryPriceCheckRequest
        @param headers: IntlFlightInventoryPriceCheckHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: IntlFlightInventoryPriceCheckResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.IntlFlightInventoryPriceCheckShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.passenger_list):
            request.passenger_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.passenger_list, 'passenger_list', 'json')
        query = {}
        if not UtilClient.is_unset(request.isv_name):
            query['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.language):
            query['language'] = request.language
        if not UtilClient.is_unset(request.order_price):
            query['order_price'] = request.order_price
        if not UtilClient.is_unset(request.ota_item_id):
            query['ota_item_id'] = request.ota_item_id
        if not UtilClient.is_unset(request.passenger_list_shrink):
            query['passenger_list'] = request.passenger_list_shrink
        if not UtilClient.is_unset(request.user_id):
            query['user_id'] = request.user_id
        if not UtilClient.is_unset(request.user_name):
            query['user_name'] = request.user_name
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='IntlFlightInventoryPriceCheck',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/intl-flight/v1/flights/action/inventory-price-check',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.IntlFlightInventoryPriceCheckResponse(),
            self.call_api(params, req, runtime)
        )

    async def intl_flight_inventory_price_check_with_options_async(
        self,
        tmp_req: btrip_open_20220520_models.IntlFlightInventoryPriceCheckRequest,
        headers: btrip_open_20220520_models.IntlFlightInventoryPriceCheckHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.IntlFlightInventoryPriceCheckResponse:
        """
        @summary 国际机票验舱验价
        
        @param tmp_req: IntlFlightInventoryPriceCheckRequest
        @param headers: IntlFlightInventoryPriceCheckHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: IntlFlightInventoryPriceCheckResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.IntlFlightInventoryPriceCheckShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.passenger_list):
            request.passenger_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.passenger_list, 'passenger_list', 'json')
        query = {}
        if not UtilClient.is_unset(request.isv_name):
            query['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.language):
            query['language'] = request.language
        if not UtilClient.is_unset(request.order_price):
            query['order_price'] = request.order_price
        if not UtilClient.is_unset(request.ota_item_id):
            query['ota_item_id'] = request.ota_item_id
        if not UtilClient.is_unset(request.passenger_list_shrink):
            query['passenger_list'] = request.passenger_list_shrink
        if not UtilClient.is_unset(request.user_id):
            query['user_id'] = request.user_id
        if not UtilClient.is_unset(request.user_name):
            query['user_name'] = request.user_name
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='IntlFlightInventoryPriceCheck',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/intl-flight/v1/flights/action/inventory-price-check',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.IntlFlightInventoryPriceCheckResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def intl_flight_inventory_price_check(
        self,
        request: btrip_open_20220520_models.IntlFlightInventoryPriceCheckRequest,
    ) -> btrip_open_20220520_models.IntlFlightInventoryPriceCheckResponse:
        """
        @summary 国际机票验舱验价
        
        @param request: IntlFlightInventoryPriceCheckRequest
        @return: IntlFlightInventoryPriceCheckResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.IntlFlightInventoryPriceCheckHeaders()
        return self.intl_flight_inventory_price_check_with_options(request, headers, runtime)

    async def intl_flight_inventory_price_check_async(
        self,
        request: btrip_open_20220520_models.IntlFlightInventoryPriceCheckRequest,
    ) -> btrip_open_20220520_models.IntlFlightInventoryPriceCheckResponse:
        """
        @summary 国际机票验舱验价
        
        @param request: IntlFlightInventoryPriceCheckRequest
        @return: IntlFlightInventoryPriceCheckResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.IntlFlightInventoryPriceCheckHeaders()
        return await self.intl_flight_inventory_price_check_with_options_async(request, headers, runtime)

    def intl_flight_listing_search_with_options(
        self,
        tmp_req: btrip_open_20220520_models.IntlFlightListingSearchRequest,
        headers: btrip_open_20220520_models.IntlFlightListingSearchHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.IntlFlightListingSearchResponse:
        """
        @summary 国际机票航班搜索
        
        @param tmp_req: IntlFlightListingSearchRequest
        @param headers: IntlFlightListingSearchHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: IntlFlightListingSearchResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.IntlFlightListingSearchShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.search_journeys):
            request.search_journeys_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.search_journeys, 'search_journeys', 'json')
        if not UtilClient.is_unset(tmp_req.search_passenger_list):
            request.search_passenger_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.search_passenger_list, 'search_passenger_list', 'json')
        query = {}
        if not UtilClient.is_unset(request.btrip_user_id):
            query['btrip_user_id'] = request.btrip_user_id
        if not UtilClient.is_unset(request.buyer_name):
            query['buyer_name'] = request.buyer_name
        if not UtilClient.is_unset(request.cabin_type):
            query['cabin_type'] = request.cabin_type
        if not UtilClient.is_unset(request.direct_only):
            query['direct_only'] = request.direct_only
        if not UtilClient.is_unset(request.isv_name):
            query['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.language):
            query['language'] = request.language
        if not UtilClient.is_unset(request.need_share_flight):
            query['need_share_flight'] = request.need_share_flight
        if not UtilClient.is_unset(request.out_wheel_search):
            query['out_wheel_search'] = request.out_wheel_search
        if not UtilClient.is_unset(request.query_record_id):
            query['query_record_id'] = request.query_record_id
        if not UtilClient.is_unset(request.search_journeys_shrink):
            query['search_journeys'] = request.search_journeys_shrink
        if not UtilClient.is_unset(request.search_mode):
            query['search_mode'] = request.search_mode
        if not UtilClient.is_unset(request.search_passenger_list_shrink):
            query['search_passenger_list'] = request.search_passenger_list_shrink
        if not UtilClient.is_unset(request.supplier_code):
            query['supplier_code'] = request.supplier_code
        if not UtilClient.is_unset(request.token):
            query['token'] = request.token
        if not UtilClient.is_unset(request.trip_type):
            query['trip_type'] = request.trip_type
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='IntlFlightListingSearch',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/intl-flight/v1/flights/action/listing-search',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.IntlFlightListingSearchResponse(),
            self.call_api(params, req, runtime)
        )

    async def intl_flight_listing_search_with_options_async(
        self,
        tmp_req: btrip_open_20220520_models.IntlFlightListingSearchRequest,
        headers: btrip_open_20220520_models.IntlFlightListingSearchHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.IntlFlightListingSearchResponse:
        """
        @summary 国际机票航班搜索
        
        @param tmp_req: IntlFlightListingSearchRequest
        @param headers: IntlFlightListingSearchHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: IntlFlightListingSearchResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.IntlFlightListingSearchShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.search_journeys):
            request.search_journeys_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.search_journeys, 'search_journeys', 'json')
        if not UtilClient.is_unset(tmp_req.search_passenger_list):
            request.search_passenger_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.search_passenger_list, 'search_passenger_list', 'json')
        query = {}
        if not UtilClient.is_unset(request.btrip_user_id):
            query['btrip_user_id'] = request.btrip_user_id
        if not UtilClient.is_unset(request.buyer_name):
            query['buyer_name'] = request.buyer_name
        if not UtilClient.is_unset(request.cabin_type):
            query['cabin_type'] = request.cabin_type
        if not UtilClient.is_unset(request.direct_only):
            query['direct_only'] = request.direct_only
        if not UtilClient.is_unset(request.isv_name):
            query['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.language):
            query['language'] = request.language
        if not UtilClient.is_unset(request.need_share_flight):
            query['need_share_flight'] = request.need_share_flight
        if not UtilClient.is_unset(request.out_wheel_search):
            query['out_wheel_search'] = request.out_wheel_search
        if not UtilClient.is_unset(request.query_record_id):
            query['query_record_id'] = request.query_record_id
        if not UtilClient.is_unset(request.search_journeys_shrink):
            query['search_journeys'] = request.search_journeys_shrink
        if not UtilClient.is_unset(request.search_mode):
            query['search_mode'] = request.search_mode
        if not UtilClient.is_unset(request.search_passenger_list_shrink):
            query['search_passenger_list'] = request.search_passenger_list_shrink
        if not UtilClient.is_unset(request.supplier_code):
            query['supplier_code'] = request.supplier_code
        if not UtilClient.is_unset(request.token):
            query['token'] = request.token
        if not UtilClient.is_unset(request.trip_type):
            query['trip_type'] = request.trip_type
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='IntlFlightListingSearch',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/intl-flight/v1/flights/action/listing-search',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.IntlFlightListingSearchResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def intl_flight_listing_search(
        self,
        request: btrip_open_20220520_models.IntlFlightListingSearchRequest,
    ) -> btrip_open_20220520_models.IntlFlightListingSearchResponse:
        """
        @summary 国际机票航班搜索
        
        @param request: IntlFlightListingSearchRequest
        @return: IntlFlightListingSearchResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.IntlFlightListingSearchHeaders()
        return self.intl_flight_listing_search_with_options(request, headers, runtime)

    async def intl_flight_listing_search_async(
        self,
        request: btrip_open_20220520_models.IntlFlightListingSearchRequest,
    ) -> btrip_open_20220520_models.IntlFlightListingSearchResponse:
        """
        @summary 国际机票航班搜索
        
        @param request: IntlFlightListingSearchRequest
        @return: IntlFlightListingSearchResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.IntlFlightListingSearchHeaders()
        return await self.intl_flight_listing_search_with_options_async(request, headers, runtime)

    def intl_flight_order_cancel_with_options(
        self,
        request: btrip_open_20220520_models.IntlFlightOrderCancelRequest,
        headers: btrip_open_20220520_models.IntlFlightOrderCancelHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.IntlFlightOrderCancelResponse:
        """
        @summary 国际机票订单取消
        
        @param request: IntlFlightOrderCancelRequest
        @param headers: IntlFlightOrderCancelHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: IntlFlightOrderCancelResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.isv_name):
            query['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.memo):
            query['memo'] = request.memo
        if not UtilClient.is_unset(request.order_id):
            query['order_id'] = request.order_id
        if not UtilClient.is_unset(request.out_order_id):
            query['out_order_id'] = request.out_order_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='IntlFlightOrderCancel',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/intl-flight/v1/order/action/cancel',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.IntlFlightOrderCancelResponse(),
            self.call_api(params, req, runtime)
        )

    async def intl_flight_order_cancel_with_options_async(
        self,
        request: btrip_open_20220520_models.IntlFlightOrderCancelRequest,
        headers: btrip_open_20220520_models.IntlFlightOrderCancelHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.IntlFlightOrderCancelResponse:
        """
        @summary 国际机票订单取消
        
        @param request: IntlFlightOrderCancelRequest
        @param headers: IntlFlightOrderCancelHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: IntlFlightOrderCancelResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.isv_name):
            query['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.memo):
            query['memo'] = request.memo
        if not UtilClient.is_unset(request.order_id):
            query['order_id'] = request.order_id
        if not UtilClient.is_unset(request.out_order_id):
            query['out_order_id'] = request.out_order_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='IntlFlightOrderCancel',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/intl-flight/v1/order/action/cancel',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.IntlFlightOrderCancelResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def intl_flight_order_cancel(
        self,
        request: btrip_open_20220520_models.IntlFlightOrderCancelRequest,
    ) -> btrip_open_20220520_models.IntlFlightOrderCancelResponse:
        """
        @summary 国际机票订单取消
        
        @param request: IntlFlightOrderCancelRequest
        @return: IntlFlightOrderCancelResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.IntlFlightOrderCancelHeaders()
        return self.intl_flight_order_cancel_with_options(request, headers, runtime)

    async def intl_flight_order_cancel_async(
        self,
        request: btrip_open_20220520_models.IntlFlightOrderCancelRequest,
    ) -> btrip_open_20220520_models.IntlFlightOrderCancelResponse:
        """
        @summary 国际机票订单取消
        
        @param request: IntlFlightOrderCancelRequest
        @return: IntlFlightOrderCancelResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.IntlFlightOrderCancelHeaders()
        return await self.intl_flight_order_cancel_with_options_async(request, headers, runtime)

    def intl_flight_order_detail_with_options(
        self,
        request: btrip_open_20220520_models.IntlFlightOrderDetailRequest,
        headers: btrip_open_20220520_models.IntlFlightOrderDetailHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.IntlFlightOrderDetailResponse:
        """
        @summary 国际机票订单详情
        
        @param request: IntlFlightOrderDetailRequest
        @param headers: IntlFlightOrderDetailHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: IntlFlightOrderDetailResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.isv_name):
            query['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.order_id):
            query['order_id'] = request.order_id
        if not UtilClient.is_unset(request.out_order_id):
            query['out_order_id'] = request.out_order_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='IntlFlightOrderDetail',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/intl-flight/v1/order/action/detail',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.IntlFlightOrderDetailResponse(),
            self.call_api(params, req, runtime)
        )

    async def intl_flight_order_detail_with_options_async(
        self,
        request: btrip_open_20220520_models.IntlFlightOrderDetailRequest,
        headers: btrip_open_20220520_models.IntlFlightOrderDetailHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.IntlFlightOrderDetailResponse:
        """
        @summary 国际机票订单详情
        
        @param request: IntlFlightOrderDetailRequest
        @param headers: IntlFlightOrderDetailHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: IntlFlightOrderDetailResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.isv_name):
            query['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.order_id):
            query['order_id'] = request.order_id
        if not UtilClient.is_unset(request.out_order_id):
            query['out_order_id'] = request.out_order_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='IntlFlightOrderDetail',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/intl-flight/v1/order/action/detail',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.IntlFlightOrderDetailResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def intl_flight_order_detail(
        self,
        request: btrip_open_20220520_models.IntlFlightOrderDetailRequest,
    ) -> btrip_open_20220520_models.IntlFlightOrderDetailResponse:
        """
        @summary 国际机票订单详情
        
        @param request: IntlFlightOrderDetailRequest
        @return: IntlFlightOrderDetailResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.IntlFlightOrderDetailHeaders()
        return self.intl_flight_order_detail_with_options(request, headers, runtime)

    async def intl_flight_order_detail_async(
        self,
        request: btrip_open_20220520_models.IntlFlightOrderDetailRequest,
    ) -> btrip_open_20220520_models.IntlFlightOrderDetailResponse:
        """
        @summary 国际机票订单详情
        
        @param request: IntlFlightOrderDetailRequest
        @return: IntlFlightOrderDetailResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.IntlFlightOrderDetailHeaders()
        return await self.intl_flight_order_detail_with_options_async(request, headers, runtime)

    def intl_flight_order_pay_with_options(
        self,
        tmp_req: btrip_open_20220520_models.IntlFlightOrderPayRequest,
        headers: btrip_open_20220520_models.IntlFlightOrderPayHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.IntlFlightOrderPayResponse:
        """
        @summary 国际机票订单支付
        
        @param tmp_req: IntlFlightOrderPayRequest
        @param headers: IntlFlightOrderPayHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: IntlFlightOrderPayResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.IntlFlightOrderPayShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.ext_params):
            request.ext_params_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.ext_params, 'ext_params', 'json')
        query = {}
        if not UtilClient.is_unset(request.ext_params_shrink):
            query['ext_params'] = request.ext_params_shrink
        if not UtilClient.is_unset(request.isv_name):
            query['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.order_id):
            query['order_id'] = request.order_id
        if not UtilClient.is_unset(request.out_order_id):
            query['out_order_id'] = request.out_order_id
        if not UtilClient.is_unset(request.total_price):
            query['total_price'] = request.total_price
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='IntlFlightOrderPay',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/intl-flight/v1/order/action/pay',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.IntlFlightOrderPayResponse(),
            self.call_api(params, req, runtime)
        )

    async def intl_flight_order_pay_with_options_async(
        self,
        tmp_req: btrip_open_20220520_models.IntlFlightOrderPayRequest,
        headers: btrip_open_20220520_models.IntlFlightOrderPayHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.IntlFlightOrderPayResponse:
        """
        @summary 国际机票订单支付
        
        @param tmp_req: IntlFlightOrderPayRequest
        @param headers: IntlFlightOrderPayHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: IntlFlightOrderPayResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.IntlFlightOrderPayShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.ext_params):
            request.ext_params_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.ext_params, 'ext_params', 'json')
        query = {}
        if not UtilClient.is_unset(request.ext_params_shrink):
            query['ext_params'] = request.ext_params_shrink
        if not UtilClient.is_unset(request.isv_name):
            query['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.order_id):
            query['order_id'] = request.order_id
        if not UtilClient.is_unset(request.out_order_id):
            query['out_order_id'] = request.out_order_id
        if not UtilClient.is_unset(request.total_price):
            query['total_price'] = request.total_price
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='IntlFlightOrderPay',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/intl-flight/v1/order/action/pay',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.IntlFlightOrderPayResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def intl_flight_order_pay(
        self,
        request: btrip_open_20220520_models.IntlFlightOrderPayRequest,
    ) -> btrip_open_20220520_models.IntlFlightOrderPayResponse:
        """
        @summary 国际机票订单支付
        
        @param request: IntlFlightOrderPayRequest
        @return: IntlFlightOrderPayResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.IntlFlightOrderPayHeaders()
        return self.intl_flight_order_pay_with_options(request, headers, runtime)

    async def intl_flight_order_pay_async(
        self,
        request: btrip_open_20220520_models.IntlFlightOrderPayRequest,
    ) -> btrip_open_20220520_models.IntlFlightOrderPayResponse:
        """
        @summary 国际机票订单支付
        
        @param request: IntlFlightOrderPayRequest
        @return: IntlFlightOrderPayResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.IntlFlightOrderPayHeaders()
        return await self.intl_flight_order_pay_with_options_async(request, headers, runtime)

    def intl_flight_order_pay_check_with_options(
        self,
        request: btrip_open_20220520_models.IntlFlightOrderPayCheckRequest,
        headers: btrip_open_20220520_models.IntlFlightOrderPayCheckHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.IntlFlightOrderPayCheckResponse:
        """
        @summary 国际机票订单支付前校验
        
        @param request: IntlFlightOrderPayCheckRequest
        @param headers: IntlFlightOrderPayCheckHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: IntlFlightOrderPayCheckResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.isv_name):
            query['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.order_id):
            query['order_id'] = request.order_id
        if not UtilClient.is_unset(request.out_order_id):
            query['out_order_id'] = request.out_order_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='IntlFlightOrderPayCheck',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/intl-flight/v1/order/action/pay-check',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.IntlFlightOrderPayCheckResponse(),
            self.call_api(params, req, runtime)
        )

    async def intl_flight_order_pay_check_with_options_async(
        self,
        request: btrip_open_20220520_models.IntlFlightOrderPayCheckRequest,
        headers: btrip_open_20220520_models.IntlFlightOrderPayCheckHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.IntlFlightOrderPayCheckResponse:
        """
        @summary 国际机票订单支付前校验
        
        @param request: IntlFlightOrderPayCheckRequest
        @param headers: IntlFlightOrderPayCheckHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: IntlFlightOrderPayCheckResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.isv_name):
            query['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.order_id):
            query['order_id'] = request.order_id
        if not UtilClient.is_unset(request.out_order_id):
            query['out_order_id'] = request.out_order_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='IntlFlightOrderPayCheck',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/intl-flight/v1/order/action/pay-check',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.IntlFlightOrderPayCheckResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def intl_flight_order_pay_check(
        self,
        request: btrip_open_20220520_models.IntlFlightOrderPayCheckRequest,
    ) -> btrip_open_20220520_models.IntlFlightOrderPayCheckResponse:
        """
        @summary 国际机票订单支付前校验
        
        @param request: IntlFlightOrderPayCheckRequest
        @return: IntlFlightOrderPayCheckResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.IntlFlightOrderPayCheckHeaders()
        return self.intl_flight_order_pay_check_with_options(request, headers, runtime)

    async def intl_flight_order_pay_check_async(
        self,
        request: btrip_open_20220520_models.IntlFlightOrderPayCheckRequest,
    ) -> btrip_open_20220520_models.IntlFlightOrderPayCheckResponse:
        """
        @summary 国际机票订单支付前校验
        
        @param request: IntlFlightOrderPayCheckRequest
        @return: IntlFlightOrderPayCheckResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.IntlFlightOrderPayCheckHeaders()
        return await self.intl_flight_order_pay_check_with_options_async(request, headers, runtime)

    def intl_flight_ota_item_detail_with_options(
        self,
        ota_item_id: str,
        request: btrip_open_20220520_models.IntlFlightOtaItemDetailRequest,
        headers: btrip_open_20220520_models.IntlFlightOtaItemDetailHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.IntlFlightOtaItemDetailResponse:
        """
        @summary 国际机票报价商品详情
        
        @param request: IntlFlightOtaItemDetailRequest
        @param headers: IntlFlightOtaItemDetailHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: IntlFlightOtaItemDetailResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.btrip_user_id):
            query['btrip_user_id'] = request.btrip_user_id
        if not UtilClient.is_unset(request.buyer_name):
            query['buyer_name'] = request.buyer_name
        if not UtilClient.is_unset(request.isv_name):
            query['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.language):
            query['language'] = request.language
        if not UtilClient.is_unset(request.supplier_code):
            query['supplier_code'] = request.supplier_code
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='IntlFlightOtaItemDetail',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/intl-flight/v1/items/{OpenApiUtilClient.get_encode_param(ota_item_id)}/action/ota-get',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.IntlFlightOtaItemDetailResponse(),
            self.call_api(params, req, runtime)
        )

    async def intl_flight_ota_item_detail_with_options_async(
        self,
        ota_item_id: str,
        request: btrip_open_20220520_models.IntlFlightOtaItemDetailRequest,
        headers: btrip_open_20220520_models.IntlFlightOtaItemDetailHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.IntlFlightOtaItemDetailResponse:
        """
        @summary 国际机票报价商品详情
        
        @param request: IntlFlightOtaItemDetailRequest
        @param headers: IntlFlightOtaItemDetailHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: IntlFlightOtaItemDetailResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.btrip_user_id):
            query['btrip_user_id'] = request.btrip_user_id
        if not UtilClient.is_unset(request.buyer_name):
            query['buyer_name'] = request.buyer_name
        if not UtilClient.is_unset(request.isv_name):
            query['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.language):
            query['language'] = request.language
        if not UtilClient.is_unset(request.supplier_code):
            query['supplier_code'] = request.supplier_code
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='IntlFlightOtaItemDetail',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/intl-flight/v1/items/{OpenApiUtilClient.get_encode_param(ota_item_id)}/action/ota-get',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.IntlFlightOtaItemDetailResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def intl_flight_ota_item_detail(
        self,
        ota_item_id: str,
        request: btrip_open_20220520_models.IntlFlightOtaItemDetailRequest,
    ) -> btrip_open_20220520_models.IntlFlightOtaItemDetailResponse:
        """
        @summary 国际机票报价商品详情
        
        @param request: IntlFlightOtaItemDetailRequest
        @return: IntlFlightOtaItemDetailResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.IntlFlightOtaItemDetailHeaders()
        return self.intl_flight_ota_item_detail_with_options(ota_item_id, request, headers, runtime)

    async def intl_flight_ota_item_detail_async(
        self,
        ota_item_id: str,
        request: btrip_open_20220520_models.IntlFlightOtaItemDetailRequest,
    ) -> btrip_open_20220520_models.IntlFlightOtaItemDetailResponse:
        """
        @summary 国际机票报价商品详情
        
        @param request: IntlFlightOtaItemDetailRequest
        @return: IntlFlightOtaItemDetailResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.IntlFlightOtaItemDetailHeaders()
        return await self.intl_flight_ota_item_detail_with_options_async(ota_item_id, request, headers, runtime)

    def intl_flight_ota_search_with_options(
        self,
        tmp_req: btrip_open_20220520_models.IntlFlightOtaSearchRequest,
        headers: btrip_open_20220520_models.IntlFlightOtaSearchHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.IntlFlightOtaSearchResponse:
        """
        @summary 国际机票航班报价查询
        
        @param tmp_req: IntlFlightOtaSearchRequest
        @param headers: IntlFlightOtaSearchHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: IntlFlightOtaSearchResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.IntlFlightOtaSearchShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.search_journeys):
            request.search_journeys_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.search_journeys, 'search_journeys', 'json')
        if not UtilClient.is_unset(tmp_req.search_passenger_list):
            request.search_passenger_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.search_passenger_list, 'search_passenger_list', 'json')
        query = {}
        if not UtilClient.is_unset(request.btrip_user_id):
            query['btrip_user_id'] = request.btrip_user_id
        if not UtilClient.is_unset(request.buyer_name):
            query['buyer_name'] = request.buyer_name
        if not UtilClient.is_unset(request.cabin_type):
            query['cabin_type'] = request.cabin_type
        if not UtilClient.is_unset(request.direct_only):
            query['direct_only'] = request.direct_only
        if not UtilClient.is_unset(request.isv_name):
            query['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.language):
            query['language'] = request.language
        if not UtilClient.is_unset(request.need_share_flight):
            query['need_share_flight'] = request.need_share_flight
        if not UtilClient.is_unset(request.search_journeys_shrink):
            query['search_journeys'] = request.search_journeys_shrink
        if not UtilClient.is_unset(request.search_passenger_list_shrink):
            query['search_passenger_list'] = request.search_passenger_list_shrink
        if not UtilClient.is_unset(request.supplier_code):
            query['supplier_code'] = request.supplier_code
        if not UtilClient.is_unset(request.trip_type):
            query['trip_type'] = request.trip_type
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='IntlFlightOtaSearch',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/intl-flight/v1/flights/action/ota-search',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.IntlFlightOtaSearchResponse(),
            self.call_api(params, req, runtime)
        )

    async def intl_flight_ota_search_with_options_async(
        self,
        tmp_req: btrip_open_20220520_models.IntlFlightOtaSearchRequest,
        headers: btrip_open_20220520_models.IntlFlightOtaSearchHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.IntlFlightOtaSearchResponse:
        """
        @summary 国际机票航班报价查询
        
        @param tmp_req: IntlFlightOtaSearchRequest
        @param headers: IntlFlightOtaSearchHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: IntlFlightOtaSearchResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.IntlFlightOtaSearchShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.search_journeys):
            request.search_journeys_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.search_journeys, 'search_journeys', 'json')
        if not UtilClient.is_unset(tmp_req.search_passenger_list):
            request.search_passenger_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.search_passenger_list, 'search_passenger_list', 'json')
        query = {}
        if not UtilClient.is_unset(request.btrip_user_id):
            query['btrip_user_id'] = request.btrip_user_id
        if not UtilClient.is_unset(request.buyer_name):
            query['buyer_name'] = request.buyer_name
        if not UtilClient.is_unset(request.cabin_type):
            query['cabin_type'] = request.cabin_type
        if not UtilClient.is_unset(request.direct_only):
            query['direct_only'] = request.direct_only
        if not UtilClient.is_unset(request.isv_name):
            query['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.language):
            query['language'] = request.language
        if not UtilClient.is_unset(request.need_share_flight):
            query['need_share_flight'] = request.need_share_flight
        if not UtilClient.is_unset(request.search_journeys_shrink):
            query['search_journeys'] = request.search_journeys_shrink
        if not UtilClient.is_unset(request.search_passenger_list_shrink):
            query['search_passenger_list'] = request.search_passenger_list_shrink
        if not UtilClient.is_unset(request.supplier_code):
            query['supplier_code'] = request.supplier_code
        if not UtilClient.is_unset(request.trip_type):
            query['trip_type'] = request.trip_type
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='IntlFlightOtaSearch',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/intl-flight/v1/flights/action/ota-search',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.IntlFlightOtaSearchResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def intl_flight_ota_search(
        self,
        request: btrip_open_20220520_models.IntlFlightOtaSearchRequest,
    ) -> btrip_open_20220520_models.IntlFlightOtaSearchResponse:
        """
        @summary 国际机票航班报价查询
        
        @param request: IntlFlightOtaSearchRequest
        @return: IntlFlightOtaSearchResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.IntlFlightOtaSearchHeaders()
        return self.intl_flight_ota_search_with_options(request, headers, runtime)

    async def intl_flight_ota_search_async(
        self,
        request: btrip_open_20220520_models.IntlFlightOtaSearchRequest,
    ) -> btrip_open_20220520_models.IntlFlightOtaSearchResponse:
        """
        @summary 国际机票航班报价查询
        
        @param request: IntlFlightOtaSearchRequest
        @return: IntlFlightOtaSearchResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.IntlFlightOtaSearchHeaders()
        return await self.intl_flight_ota_search_with_options_async(request, headers, runtime)

    def intl_flight_segment_available_cert_with_options(
        self,
        ota_item_id: str,
        request: btrip_open_20220520_models.IntlFlightSegmentAvailableCertRequest,
        headers: btrip_open_20220520_models.IntlFlightSegmentAvailableCertHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.IntlFlightSegmentAvailableCertResponse:
        """
        @summary 国际机票航班可用证件查询
        
        @param request: IntlFlightSegmentAvailableCertRequest
        @param headers: IntlFlightSegmentAvailableCertHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: IntlFlightSegmentAvailableCertResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.isv_name):
            query['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.language):
            query['language'] = request.language
        if not UtilClient.is_unset(request.user_id):
            query['user_id'] = request.user_id
        if not UtilClient.is_unset(request.user_name):
            query['user_name'] = request.user_name
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='IntlFlightSegmentAvailableCert',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/intl-flight/v1/items/{OpenApiUtilClient.get_encode_param(ota_item_id)}/action/segment-available-cert',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.IntlFlightSegmentAvailableCertResponse(),
            self.call_api(params, req, runtime)
        )

    async def intl_flight_segment_available_cert_with_options_async(
        self,
        ota_item_id: str,
        request: btrip_open_20220520_models.IntlFlightSegmentAvailableCertRequest,
        headers: btrip_open_20220520_models.IntlFlightSegmentAvailableCertHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.IntlFlightSegmentAvailableCertResponse:
        """
        @summary 国际机票航班可用证件查询
        
        @param request: IntlFlightSegmentAvailableCertRequest
        @param headers: IntlFlightSegmentAvailableCertHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: IntlFlightSegmentAvailableCertResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.isv_name):
            query['isv_name'] = request.isv_name
        if not UtilClient.is_unset(request.language):
            query['language'] = request.language
        if not UtilClient.is_unset(request.user_id):
            query['user_id'] = request.user_id
        if not UtilClient.is_unset(request.user_name):
            query['user_name'] = request.user_name
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='IntlFlightSegmentAvailableCert',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/intl-flight/v1/items/{OpenApiUtilClient.get_encode_param(ota_item_id)}/action/segment-available-cert',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.IntlFlightSegmentAvailableCertResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def intl_flight_segment_available_cert(
        self,
        ota_item_id: str,
        request: btrip_open_20220520_models.IntlFlightSegmentAvailableCertRequest,
    ) -> btrip_open_20220520_models.IntlFlightSegmentAvailableCertResponse:
        """
        @summary 国际机票航班可用证件查询
        
        @param request: IntlFlightSegmentAvailableCertRequest
        @return: IntlFlightSegmentAvailableCertResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.IntlFlightSegmentAvailableCertHeaders()
        return self.intl_flight_segment_available_cert_with_options(ota_item_id, request, headers, runtime)

    async def intl_flight_segment_available_cert_async(
        self,
        ota_item_id: str,
        request: btrip_open_20220520_models.IntlFlightSegmentAvailableCertRequest,
    ) -> btrip_open_20220520_models.IntlFlightSegmentAvailableCertResponse:
        """
        @summary 国际机票航班可用证件查询
        
        @param request: IntlFlightSegmentAvailableCertRequest
        @return: IntlFlightSegmentAvailableCertResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.IntlFlightSegmentAvailableCertHeaders()
        return await self.intl_flight_segment_available_cert_with_options_async(ota_item_id, request, headers, runtime)

    def invoice_add_with_options(
        self,
        request: btrip_open_20220520_models.InvoiceAddRequest,
        headers: btrip_open_20220520_models.InvoiceAddHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.InvoiceAddResponse:
        """
        @summary 新增发票配置
        
        @param request: InvoiceAddRequest
        @param headers: InvoiceAddHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: InvoiceAddResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.address):
            body['address'] = request.address
        if not UtilClient.is_unset(request.bank_name):
            body['bank_name'] = request.bank_name
        if not UtilClient.is_unset(request.bank_no):
            body['bank_no'] = request.bank_no
        if not UtilClient.is_unset(request.tax_no):
            body['tax_no'] = request.tax_no
        if not UtilClient.is_unset(request.tel):
            body['tel'] = request.tel
        if not UtilClient.is_unset(request.third_part_id):
            body['third_part_id'] = request.third_part_id
        if not UtilClient.is_unset(request.title):
            body['title'] = request.title
        if not UtilClient.is_unset(request.type):
            body['type'] = request.type
        if not UtilClient.is_unset(request.unit_type):
            body['unit_type'] = request.unit_type
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='InvoiceAdd',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/invoice/v1/add-invoice',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.InvoiceAddResponse(),
            self.call_api(params, req, runtime)
        )

    async def invoice_add_with_options_async(
        self,
        request: btrip_open_20220520_models.InvoiceAddRequest,
        headers: btrip_open_20220520_models.InvoiceAddHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.InvoiceAddResponse:
        """
        @summary 新增发票配置
        
        @param request: InvoiceAddRequest
        @param headers: InvoiceAddHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: InvoiceAddResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.address):
            body['address'] = request.address
        if not UtilClient.is_unset(request.bank_name):
            body['bank_name'] = request.bank_name
        if not UtilClient.is_unset(request.bank_no):
            body['bank_no'] = request.bank_no
        if not UtilClient.is_unset(request.tax_no):
            body['tax_no'] = request.tax_no
        if not UtilClient.is_unset(request.tel):
            body['tel'] = request.tel
        if not UtilClient.is_unset(request.third_part_id):
            body['third_part_id'] = request.third_part_id
        if not UtilClient.is_unset(request.title):
            body['title'] = request.title
        if not UtilClient.is_unset(request.type):
            body['type'] = request.type
        if not UtilClient.is_unset(request.unit_type):
            body['unit_type'] = request.unit_type
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='InvoiceAdd',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/invoice/v1/add-invoice',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.InvoiceAddResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def invoice_add(
        self,
        request: btrip_open_20220520_models.InvoiceAddRequest,
    ) -> btrip_open_20220520_models.InvoiceAddResponse:
        """
        @summary 新增发票配置
        
        @param request: InvoiceAddRequest
        @return: InvoiceAddResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.InvoiceAddHeaders()
        return self.invoice_add_with_options(request, headers, runtime)

    async def invoice_add_async(
        self,
        request: btrip_open_20220520_models.InvoiceAddRequest,
    ) -> btrip_open_20220520_models.InvoiceAddResponse:
        """
        @summary 新增发票配置
        
        @param request: InvoiceAddRequest
        @return: InvoiceAddResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.InvoiceAddHeaders()
        return await self.invoice_add_with_options_async(request, headers, runtime)

    def invoice_delete_with_options(
        self,
        request: btrip_open_20220520_models.InvoiceDeleteRequest,
        headers: btrip_open_20220520_models.InvoiceDeleteHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.InvoiceDeleteResponse:
        """
        @summary 删除发票抬头
        
        @param request: InvoiceDeleteRequest
        @param headers: InvoiceDeleteHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: InvoiceDeleteResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.third_part_id):
            query['third_part_id'] = request.third_part_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='InvoiceDelete',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/invoice/v1/invoice',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.InvoiceDeleteResponse(),
            self.call_api(params, req, runtime)
        )

    async def invoice_delete_with_options_async(
        self,
        request: btrip_open_20220520_models.InvoiceDeleteRequest,
        headers: btrip_open_20220520_models.InvoiceDeleteHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.InvoiceDeleteResponse:
        """
        @summary 删除发票抬头
        
        @param request: InvoiceDeleteRequest
        @param headers: InvoiceDeleteHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: InvoiceDeleteResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.third_part_id):
            query['third_part_id'] = request.third_part_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='InvoiceDelete',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/invoice/v1/invoice',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.InvoiceDeleteResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def invoice_delete(
        self,
        request: btrip_open_20220520_models.InvoiceDeleteRequest,
    ) -> btrip_open_20220520_models.InvoiceDeleteResponse:
        """
        @summary 删除发票抬头
        
        @param request: InvoiceDeleteRequest
        @return: InvoiceDeleteResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.InvoiceDeleteHeaders()
        return self.invoice_delete_with_options(request, headers, runtime)

    async def invoice_delete_async(
        self,
        request: btrip_open_20220520_models.InvoiceDeleteRequest,
    ) -> btrip_open_20220520_models.InvoiceDeleteResponse:
        """
        @summary 删除发票抬头
        
        @param request: InvoiceDeleteRequest
        @return: InvoiceDeleteResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.InvoiceDeleteHeaders()
        return await self.invoice_delete_with_options_async(request, headers, runtime)

    def invoice_modify_with_options(
        self,
        request: btrip_open_20220520_models.InvoiceModifyRequest,
        headers: btrip_open_20220520_models.InvoiceModifyHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.InvoiceModifyResponse:
        """
        @summary 修改发票配置
        
        @param request: InvoiceModifyRequest
        @param headers: InvoiceModifyHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: InvoiceModifyResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.address):
            body['address'] = request.address
        if not UtilClient.is_unset(request.bank_name):
            body['bank_name'] = request.bank_name
        if not UtilClient.is_unset(request.bank_no):
            body['bank_no'] = request.bank_no
        if not UtilClient.is_unset(request.tax_no):
            body['tax_no'] = request.tax_no
        if not UtilClient.is_unset(request.tel):
            body['tel'] = request.tel
        if not UtilClient.is_unset(request.third_part_id):
            body['third_part_id'] = request.third_part_id
        if not UtilClient.is_unset(request.title):
            body['title'] = request.title
        if not UtilClient.is_unset(request.type):
            body['type'] = request.type
        if not UtilClient.is_unset(request.unit_type):
            body['unit_type'] = request.unit_type
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='InvoiceModify',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/invoice/v1/invoice',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.InvoiceModifyResponse(),
            self.call_api(params, req, runtime)
        )

    async def invoice_modify_with_options_async(
        self,
        request: btrip_open_20220520_models.InvoiceModifyRequest,
        headers: btrip_open_20220520_models.InvoiceModifyHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.InvoiceModifyResponse:
        """
        @summary 修改发票配置
        
        @param request: InvoiceModifyRequest
        @param headers: InvoiceModifyHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: InvoiceModifyResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.address):
            body['address'] = request.address
        if not UtilClient.is_unset(request.bank_name):
            body['bank_name'] = request.bank_name
        if not UtilClient.is_unset(request.bank_no):
            body['bank_no'] = request.bank_no
        if not UtilClient.is_unset(request.tax_no):
            body['tax_no'] = request.tax_no
        if not UtilClient.is_unset(request.tel):
            body['tel'] = request.tel
        if not UtilClient.is_unset(request.third_part_id):
            body['third_part_id'] = request.third_part_id
        if not UtilClient.is_unset(request.title):
            body['title'] = request.title
        if not UtilClient.is_unset(request.type):
            body['type'] = request.type
        if not UtilClient.is_unset(request.unit_type):
            body['unit_type'] = request.unit_type
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='InvoiceModify',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/invoice/v1/invoice',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.InvoiceModifyResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def invoice_modify(
        self,
        request: btrip_open_20220520_models.InvoiceModifyRequest,
    ) -> btrip_open_20220520_models.InvoiceModifyResponse:
        """
        @summary 修改发票配置
        
        @param request: InvoiceModifyRequest
        @return: InvoiceModifyResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.InvoiceModifyHeaders()
        return self.invoice_modify_with_options(request, headers, runtime)

    async def invoice_modify_async(
        self,
        request: btrip_open_20220520_models.InvoiceModifyRequest,
    ) -> btrip_open_20220520_models.InvoiceModifyResponse:
        """
        @summary 修改发票配置
        
        @param request: InvoiceModifyRequest
        @return: InvoiceModifyResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.InvoiceModifyHeaders()
        return await self.invoice_modify_with_options_async(request, headers, runtime)

    def invoice_rule_add_with_options(
        self,
        tmp_req: btrip_open_20220520_models.InvoiceRuleAddRequest,
        headers: btrip_open_20220520_models.InvoiceRuleAddHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.InvoiceRuleAddResponse:
        """
        @summary 新增发票抬头可用员工
        
        @param tmp_req: InvoiceRuleAddRequest
        @param headers: InvoiceRuleAddHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: InvoiceRuleAddResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.InvoiceRuleAddShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.entities):
            request.entities_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.entities, 'entities', 'json')
        body = {}
        if not UtilClient.is_unset(request.entities_shrink):
            body['entities'] = request.entities_shrink
        if not UtilClient.is_unset(request.third_part_id):
            body['third_part_id'] = request.third_part_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='InvoiceRuleAdd',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/invoice/v1/invoice-rule',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.InvoiceRuleAddResponse(),
            self.call_api(params, req, runtime)
        )

    async def invoice_rule_add_with_options_async(
        self,
        tmp_req: btrip_open_20220520_models.InvoiceRuleAddRequest,
        headers: btrip_open_20220520_models.InvoiceRuleAddHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.InvoiceRuleAddResponse:
        """
        @summary 新增发票抬头可用员工
        
        @param tmp_req: InvoiceRuleAddRequest
        @param headers: InvoiceRuleAddHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: InvoiceRuleAddResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.InvoiceRuleAddShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.entities):
            request.entities_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.entities, 'entities', 'json')
        body = {}
        if not UtilClient.is_unset(request.entities_shrink):
            body['entities'] = request.entities_shrink
        if not UtilClient.is_unset(request.third_part_id):
            body['third_part_id'] = request.third_part_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='InvoiceRuleAdd',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/invoice/v1/invoice-rule',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.InvoiceRuleAddResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def invoice_rule_add(
        self,
        request: btrip_open_20220520_models.InvoiceRuleAddRequest,
    ) -> btrip_open_20220520_models.InvoiceRuleAddResponse:
        """
        @summary 新增发票抬头可用员工
        
        @param request: InvoiceRuleAddRequest
        @return: InvoiceRuleAddResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.InvoiceRuleAddHeaders()
        return self.invoice_rule_add_with_options(request, headers, runtime)

    async def invoice_rule_add_async(
        self,
        request: btrip_open_20220520_models.InvoiceRuleAddRequest,
    ) -> btrip_open_20220520_models.InvoiceRuleAddResponse:
        """
        @summary 新增发票抬头可用员工
        
        @param request: InvoiceRuleAddRequest
        @return: InvoiceRuleAddResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.InvoiceRuleAddHeaders()
        return await self.invoice_rule_add_with_options_async(request, headers, runtime)

    def invoice_rule_delete_with_options(
        self,
        tmp_req: btrip_open_20220520_models.InvoiceRuleDeleteRequest,
        headers: btrip_open_20220520_models.InvoiceRuleDeleteHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.InvoiceRuleDeleteResponse:
        """
        @summary 删除发票抬头可用员工
        
        @param tmp_req: InvoiceRuleDeleteRequest
        @param headers: InvoiceRuleDeleteHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: InvoiceRuleDeleteResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.InvoiceRuleDeleteShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.entities):
            request.entities_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.entities, 'entities', 'json')
        query = {}
        if not UtilClient.is_unset(request.del_all):
            query['del_all'] = request.del_all
        if not UtilClient.is_unset(request.entities_shrink):
            query['entities'] = request.entities_shrink
        if not UtilClient.is_unset(request.third_part_id):
            query['third_part_id'] = request.third_part_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='InvoiceRuleDelete',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/invoice/v1/invoice-rule',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.InvoiceRuleDeleteResponse(),
            self.call_api(params, req, runtime)
        )

    async def invoice_rule_delete_with_options_async(
        self,
        tmp_req: btrip_open_20220520_models.InvoiceRuleDeleteRequest,
        headers: btrip_open_20220520_models.InvoiceRuleDeleteHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.InvoiceRuleDeleteResponse:
        """
        @summary 删除发票抬头可用员工
        
        @param tmp_req: InvoiceRuleDeleteRequest
        @param headers: InvoiceRuleDeleteHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: InvoiceRuleDeleteResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.InvoiceRuleDeleteShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.entities):
            request.entities_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.entities, 'entities', 'json')
        query = {}
        if not UtilClient.is_unset(request.del_all):
            query['del_all'] = request.del_all
        if not UtilClient.is_unset(request.entities_shrink):
            query['entities'] = request.entities_shrink
        if not UtilClient.is_unset(request.third_part_id):
            query['third_part_id'] = request.third_part_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='InvoiceRuleDelete',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/invoice/v1/invoice-rule',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.InvoiceRuleDeleteResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def invoice_rule_delete(
        self,
        request: btrip_open_20220520_models.InvoiceRuleDeleteRequest,
    ) -> btrip_open_20220520_models.InvoiceRuleDeleteResponse:
        """
        @summary 删除发票抬头可用员工
        
        @param request: InvoiceRuleDeleteRequest
        @return: InvoiceRuleDeleteResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.InvoiceRuleDeleteHeaders()
        return self.invoice_rule_delete_with_options(request, headers, runtime)

    async def invoice_rule_delete_async(
        self,
        request: btrip_open_20220520_models.InvoiceRuleDeleteRequest,
    ) -> btrip_open_20220520_models.InvoiceRuleDeleteResponse:
        """
        @summary 删除发票抬头可用员工
        
        @param request: InvoiceRuleDeleteRequest
        @return: InvoiceRuleDeleteResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.InvoiceRuleDeleteHeaders()
        return await self.invoice_rule_delete_with_options_async(request, headers, runtime)

    def invoice_rule_save_with_options(
        self,
        tmp_req: btrip_open_20220520_models.InvoiceRuleSaveRequest,
        headers: btrip_open_20220520_models.InvoiceRuleSaveHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.InvoiceRuleSaveResponse:
        """
        @summary 保存发票规则
        
        @param tmp_req: InvoiceRuleSaveRequest
        @param headers: InvoiceRuleSaveHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: InvoiceRuleSaveResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.InvoiceRuleSaveShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.entities):
            request.entities_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.entities, 'entities', 'json')
        body = {}
        if not UtilClient.is_unset(request.all_employe):
            body['all_employe'] = request.all_employe
        if not UtilClient.is_unset(request.entities_shrink):
            body['entities'] = request.entities_shrink
        if not UtilClient.is_unset(request.scope):
            body['scope'] = request.scope
        if not UtilClient.is_unset(request.third_part_id):
            body['third_part_id'] = request.third_part_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='InvoiceRuleSave',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/invoice/v1/invoice-rule',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.InvoiceRuleSaveResponse(),
            self.call_api(params, req, runtime)
        )

    async def invoice_rule_save_with_options_async(
        self,
        tmp_req: btrip_open_20220520_models.InvoiceRuleSaveRequest,
        headers: btrip_open_20220520_models.InvoiceRuleSaveHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.InvoiceRuleSaveResponse:
        """
        @summary 保存发票规则
        
        @param tmp_req: InvoiceRuleSaveRequest
        @param headers: InvoiceRuleSaveHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: InvoiceRuleSaveResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.InvoiceRuleSaveShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.entities):
            request.entities_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.entities, 'entities', 'json')
        body = {}
        if not UtilClient.is_unset(request.all_employe):
            body['all_employe'] = request.all_employe
        if not UtilClient.is_unset(request.entities_shrink):
            body['entities'] = request.entities_shrink
        if not UtilClient.is_unset(request.scope):
            body['scope'] = request.scope
        if not UtilClient.is_unset(request.third_part_id):
            body['third_part_id'] = request.third_part_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='InvoiceRuleSave',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/invoice/v1/invoice-rule',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.InvoiceRuleSaveResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def invoice_rule_save(
        self,
        request: btrip_open_20220520_models.InvoiceRuleSaveRequest,
    ) -> btrip_open_20220520_models.InvoiceRuleSaveResponse:
        """
        @summary 保存发票规则
        
        @param request: InvoiceRuleSaveRequest
        @return: InvoiceRuleSaveResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.InvoiceRuleSaveHeaders()
        return self.invoice_rule_save_with_options(request, headers, runtime)

    async def invoice_rule_save_async(
        self,
        request: btrip_open_20220520_models.InvoiceRuleSaveRequest,
    ) -> btrip_open_20220520_models.InvoiceRuleSaveResponse:
        """
        @summary 保存发票规则
        
        @param request: InvoiceRuleSaveRequest
        @return: InvoiceRuleSaveResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.InvoiceRuleSaveHeaders()
        return await self.invoice_rule_save_with_options_async(request, headers, runtime)

    def invoice_search_with_options(
        self,
        request: btrip_open_20220520_models.InvoiceSearchRequest,
        headers: btrip_open_20220520_models.InvoiceSearchHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.InvoiceSearchResponse:
        """
        @summary 搜索用户可用发票抬头
        
        @param request: InvoiceSearchRequest
        @param headers: InvoiceSearchHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: InvoiceSearchResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.third_part_id):
            query['third_part_id'] = request.third_part_id
        if not UtilClient.is_unset(request.title):
            query['title'] = request.title
        if not UtilClient.is_unset(request.user_id):
            query['user_id'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='InvoiceSearch',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/invoice/v1/invoice',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.InvoiceSearchResponse(),
            self.call_api(params, req, runtime)
        )

    async def invoice_search_with_options_async(
        self,
        request: btrip_open_20220520_models.InvoiceSearchRequest,
        headers: btrip_open_20220520_models.InvoiceSearchHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.InvoiceSearchResponse:
        """
        @summary 搜索用户可用发票抬头
        
        @param request: InvoiceSearchRequest
        @param headers: InvoiceSearchHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: InvoiceSearchResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.third_part_id):
            query['third_part_id'] = request.third_part_id
        if not UtilClient.is_unset(request.title):
            query['title'] = request.title
        if not UtilClient.is_unset(request.user_id):
            query['user_id'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='InvoiceSearch',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/invoice/v1/invoice',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.InvoiceSearchResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def invoice_search(
        self,
        request: btrip_open_20220520_models.InvoiceSearchRequest,
    ) -> btrip_open_20220520_models.InvoiceSearchResponse:
        """
        @summary 搜索用户可用发票抬头
        
        @param request: InvoiceSearchRequest
        @return: InvoiceSearchResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.InvoiceSearchHeaders()
        return self.invoice_search_with_options(request, headers, runtime)

    async def invoice_search_async(
        self,
        request: btrip_open_20220520_models.InvoiceSearchRequest,
    ) -> btrip_open_20220520_models.InvoiceSearchResponse:
        """
        @summary 搜索用户可用发票抬头
        
        @param request: InvoiceSearchRequest
        @return: InvoiceSearchResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.InvoiceSearchHeaders()
        return await self.invoice_search_with_options_async(request, headers, runtime)

    def isv_rule_save_with_options(
        self,
        tmp_req: btrip_open_20220520_models.IsvRuleSaveRequest,
        headers: btrip_open_20220520_models.IsvRuleSaveHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.IsvRuleSaveResponse:
        """
        @summary 员工特殊角色修改
        
        @param tmp_req: IsvRuleSaveRequest
        @param headers: IsvRuleSaveHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: IsvRuleSaveResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.IsvRuleSaveShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.bookuser_list):
            request.bookuser_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.bookuser_list, 'bookuser_list', 'json')
        body = {}
        if not UtilClient.is_unset(request.apply_need):
            body['apply_need'] = request.apply_need
        if not UtilClient.is_unset(request.book_type):
            body['book_type'] = request.book_type
        if not UtilClient.is_unset(request.bookuser_list_shrink):
            body['bookuser_list'] = request.bookuser_list_shrink
        if not UtilClient.is_unset(request.rule_need):
            body['rule_need'] = request.rule_need
        if not UtilClient.is_unset(request.status):
            body['status'] = request.status
        if not UtilClient.is_unset(request.user_id):
            body['user_id'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='IsvRuleSave',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/user/v1/rule',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.IsvRuleSaveResponse(),
            self.call_api(params, req, runtime)
        )

    async def isv_rule_save_with_options_async(
        self,
        tmp_req: btrip_open_20220520_models.IsvRuleSaveRequest,
        headers: btrip_open_20220520_models.IsvRuleSaveHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.IsvRuleSaveResponse:
        """
        @summary 员工特殊角色修改
        
        @param tmp_req: IsvRuleSaveRequest
        @param headers: IsvRuleSaveHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: IsvRuleSaveResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.IsvRuleSaveShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.bookuser_list):
            request.bookuser_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.bookuser_list, 'bookuser_list', 'json')
        body = {}
        if not UtilClient.is_unset(request.apply_need):
            body['apply_need'] = request.apply_need
        if not UtilClient.is_unset(request.book_type):
            body['book_type'] = request.book_type
        if not UtilClient.is_unset(request.bookuser_list_shrink):
            body['bookuser_list'] = request.bookuser_list_shrink
        if not UtilClient.is_unset(request.rule_need):
            body['rule_need'] = request.rule_need
        if not UtilClient.is_unset(request.status):
            body['status'] = request.status
        if not UtilClient.is_unset(request.user_id):
            body['user_id'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='IsvRuleSave',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/user/v1/rule',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.IsvRuleSaveResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def isv_rule_save(
        self,
        request: btrip_open_20220520_models.IsvRuleSaveRequest,
    ) -> btrip_open_20220520_models.IsvRuleSaveResponse:
        """
        @summary 员工特殊角色修改
        
        @param request: IsvRuleSaveRequest
        @return: IsvRuleSaveResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.IsvRuleSaveHeaders()
        return self.isv_rule_save_with_options(request, headers, runtime)

    async def isv_rule_save_async(
        self,
        request: btrip_open_20220520_models.IsvRuleSaveRequest,
    ) -> btrip_open_20220520_models.IsvRuleSaveResponse:
        """
        @summary 员工特殊角色修改
        
        @param request: IsvRuleSaveRequest
        @return: IsvRuleSaveResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.IsvRuleSaveHeaders()
        return await self.isv_rule_save_with_options_async(request, headers, runtime)

    def isv_user_save_with_options(
        self,
        tmp_req: btrip_open_20220520_models.IsvUserSaveRequest,
        headers: btrip_open_20220520_models.IsvUserSaveHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.IsvUserSaveResponse:
        """
        @summary 用户同步
        
        @param tmp_req: IsvUserSaveRequest
        @param headers: IsvUserSaveHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: IsvUserSaveResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.IsvUserSaveShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.user_list):
            request.user_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.user_list, 'user_list', 'json')
        body = {}
        if not UtilClient.is_unset(request.user_list_shrink):
            body['user_list'] = request.user_list_shrink
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='IsvUserSave',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/isvuser/v1/isvuser',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.IsvUserSaveResponse(),
            self.call_api(params, req, runtime)
        )

    async def isv_user_save_with_options_async(
        self,
        tmp_req: btrip_open_20220520_models.IsvUserSaveRequest,
        headers: btrip_open_20220520_models.IsvUserSaveHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.IsvUserSaveResponse:
        """
        @summary 用户同步
        
        @param tmp_req: IsvUserSaveRequest
        @param headers: IsvUserSaveHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: IsvUserSaveResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.IsvUserSaveShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.user_list):
            request.user_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.user_list, 'user_list', 'json')
        body = {}
        if not UtilClient.is_unset(request.user_list_shrink):
            body['user_list'] = request.user_list_shrink
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='IsvUserSave',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/isvuser/v1/isvuser',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.IsvUserSaveResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def isv_user_save(
        self,
        request: btrip_open_20220520_models.IsvUserSaveRequest,
    ) -> btrip_open_20220520_models.IsvUserSaveResponse:
        """
        @summary 用户同步
        
        @param request: IsvUserSaveRequest
        @return: IsvUserSaveResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.IsvUserSaveHeaders()
        return self.isv_user_save_with_options(request, headers, runtime)

    async def isv_user_save_async(
        self,
        request: btrip_open_20220520_models.IsvUserSaveRequest,
    ) -> btrip_open_20220520_models.IsvUserSaveResponse:
        """
        @summary 用户同步
        
        @param request: IsvUserSaveRequest
        @return: IsvUserSaveResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.IsvUserSaveHeaders()
        return await self.isv_user_save_with_options_async(request, headers, runtime)

    def meal_bill_settlement_query_with_options(
        self,
        request: btrip_open_20220520_models.MealBillSettlementQueryRequest,
        headers: btrip_open_20220520_models.MealBillSettlementQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.MealBillSettlementQueryResponse:
        """
        @summary 查询因公用餐记账数据
        
        @param request: MealBillSettlementQueryRequest
        @param headers: MealBillSettlementQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: MealBillSettlementQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.page_no):
            query['page_no'] = request.page_no
        if not UtilClient.is_unset(request.page_size):
            query['page_size'] = request.page_size
        if not UtilClient.is_unset(request.period_end):
            query['period_end'] = request.period_end
        if not UtilClient.is_unset(request.period_start):
            query['period_start'] = request.period_start
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='MealBillSettlementQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/meal/v1/bill-settlement',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.MealBillSettlementQueryResponse(),
            self.call_api(params, req, runtime)
        )

    async def meal_bill_settlement_query_with_options_async(
        self,
        request: btrip_open_20220520_models.MealBillSettlementQueryRequest,
        headers: btrip_open_20220520_models.MealBillSettlementQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.MealBillSettlementQueryResponse:
        """
        @summary 查询因公用餐记账数据
        
        @param request: MealBillSettlementQueryRequest
        @param headers: MealBillSettlementQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: MealBillSettlementQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.page_no):
            query['page_no'] = request.page_no
        if not UtilClient.is_unset(request.page_size):
            query['page_size'] = request.page_size
        if not UtilClient.is_unset(request.period_end):
            query['period_end'] = request.period_end
        if not UtilClient.is_unset(request.period_start):
            query['period_start'] = request.period_start
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='MealBillSettlementQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/meal/v1/bill-settlement',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.MealBillSettlementQueryResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def meal_bill_settlement_query(
        self,
        request: btrip_open_20220520_models.MealBillSettlementQueryRequest,
    ) -> btrip_open_20220520_models.MealBillSettlementQueryResponse:
        """
        @summary 查询因公用餐记账数据
        
        @param request: MealBillSettlementQueryRequest
        @return: MealBillSettlementQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.MealBillSettlementQueryHeaders()
        return self.meal_bill_settlement_query_with_options(request, headers, runtime)

    async def meal_bill_settlement_query_async(
        self,
        request: btrip_open_20220520_models.MealBillSettlementQueryRequest,
    ) -> btrip_open_20220520_models.MealBillSettlementQueryResponse:
        """
        @summary 查询因公用餐记账数据
        
        @param request: MealBillSettlementQueryRequest
        @return: MealBillSettlementQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.MealBillSettlementQueryHeaders()
        return await self.meal_bill_settlement_query_with_options_async(request, headers, runtime)

    def meal_order_detail_query_with_options(
        self,
        order_id: str,
        request: btrip_open_20220520_models.MealOrderDetailQueryRequest,
        headers: btrip_open_20220520_models.MealOrderDetailQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.MealOrderDetailQueryResponse:
        """
        @summary 获取用餐订单详情
        
        @param request: MealOrderDetailQueryRequest
        @param headers: MealOrderDetailQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: MealOrderDetailQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.user_id):
            query['user_id'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='MealOrderDetailQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/meal/v1/orders/{OpenApiUtilClient.get_encode_param(order_id)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.MealOrderDetailQueryResponse(),
            self.call_api(params, req, runtime)
        )

    async def meal_order_detail_query_with_options_async(
        self,
        order_id: str,
        request: btrip_open_20220520_models.MealOrderDetailQueryRequest,
        headers: btrip_open_20220520_models.MealOrderDetailQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.MealOrderDetailQueryResponse:
        """
        @summary 获取用餐订单详情
        
        @param request: MealOrderDetailQueryRequest
        @param headers: MealOrderDetailQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: MealOrderDetailQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.user_id):
            query['user_id'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='MealOrderDetailQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/meal/v1/orders/{OpenApiUtilClient.get_encode_param(order_id)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.MealOrderDetailQueryResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def meal_order_detail_query(
        self,
        order_id: str,
        request: btrip_open_20220520_models.MealOrderDetailQueryRequest,
    ) -> btrip_open_20220520_models.MealOrderDetailQueryResponse:
        """
        @summary 获取用餐订单详情
        
        @param request: MealOrderDetailQueryRequest
        @return: MealOrderDetailQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.MealOrderDetailQueryHeaders()
        return self.meal_order_detail_query_with_options(order_id, request, headers, runtime)

    async def meal_order_detail_query_async(
        self,
        order_id: str,
        request: btrip_open_20220520_models.MealOrderDetailQueryRequest,
    ) -> btrip_open_20220520_models.MealOrderDetailQueryResponse:
        """
        @summary 获取用餐订单详情
        
        @param request: MealOrderDetailQueryRequest
        @return: MealOrderDetailQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.MealOrderDetailQueryHeaders()
        return await self.meal_order_detail_query_with_options_async(order_id, request, headers, runtime)

    def meal_order_list_query_with_options(
        self,
        request: btrip_open_20220520_models.MealOrderListQueryRequest,
        headers: btrip_open_20220520_models.MealOrderListQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.MealOrderListQueryResponse:
        """
        @summary 获取用餐订单列表
        
        @param request: MealOrderListQueryRequest
        @param headers: MealOrderListQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: MealOrderListQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.user_id):
            query['user_id'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='MealOrderListQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/meal/v1/orders',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.MealOrderListQueryResponse(),
            self.call_api(params, req, runtime)
        )

    async def meal_order_list_query_with_options_async(
        self,
        request: btrip_open_20220520_models.MealOrderListQueryRequest,
        headers: btrip_open_20220520_models.MealOrderListQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.MealOrderListQueryResponse:
        """
        @summary 获取用餐订单列表
        
        @param request: MealOrderListQueryRequest
        @param headers: MealOrderListQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: MealOrderListQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.user_id):
            query['user_id'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='MealOrderListQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/meal/v1/orders',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.MealOrderListQueryResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def meal_order_list_query(
        self,
        request: btrip_open_20220520_models.MealOrderListQueryRequest,
    ) -> btrip_open_20220520_models.MealOrderListQueryResponse:
        """
        @summary 获取用餐订单列表
        
        @param request: MealOrderListQueryRequest
        @return: MealOrderListQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.MealOrderListQueryHeaders()
        return self.meal_order_list_query_with_options(request, headers, runtime)

    async def meal_order_list_query_async(
        self,
        request: btrip_open_20220520_models.MealOrderListQueryRequest,
    ) -> btrip_open_20220520_models.MealOrderListQueryResponse:
        """
        @summary 获取用餐订单列表
        
        @param request: MealOrderListQueryRequest
        @return: MealOrderListQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.MealOrderListQueryHeaders()
        return await self.meal_order_list_query_with_options_async(request, headers, runtime)

    def month_bill_confirm_with_options(
        self,
        request: btrip_open_20220520_models.MonthBillConfirmRequest,
        headers: btrip_open_20220520_models.MonthBillConfirmHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.MonthBillConfirmResponse:
        """
        @summary 月账单确认
        
        @param request: MonthBillConfirmRequest
        @param headers: MonthBillConfirmHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: MonthBillConfirmResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.mail_bill_date):
            body['mail_bill_date'] = request.mail_bill_date
        if not UtilClient.is_unset(request.user_id):
            body['user_id'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='MonthBillConfirm',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/bill/v1/status/action/confirm',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.MonthBillConfirmResponse(),
            self.call_api(params, req, runtime)
        )

    async def month_bill_confirm_with_options_async(
        self,
        request: btrip_open_20220520_models.MonthBillConfirmRequest,
        headers: btrip_open_20220520_models.MonthBillConfirmHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.MonthBillConfirmResponse:
        """
        @summary 月账单确认
        
        @param request: MonthBillConfirmRequest
        @param headers: MonthBillConfirmHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: MonthBillConfirmResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.mail_bill_date):
            body['mail_bill_date'] = request.mail_bill_date
        if not UtilClient.is_unset(request.user_id):
            body['user_id'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='MonthBillConfirm',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/bill/v1/status/action/confirm',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.MonthBillConfirmResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def month_bill_confirm(
        self,
        request: btrip_open_20220520_models.MonthBillConfirmRequest,
    ) -> btrip_open_20220520_models.MonthBillConfirmResponse:
        """
        @summary 月账单确认
        
        @param request: MonthBillConfirmRequest
        @return: MonthBillConfirmResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.MonthBillConfirmHeaders()
        return self.month_bill_confirm_with_options(request, headers, runtime)

    async def month_bill_confirm_async(
        self,
        request: btrip_open_20220520_models.MonthBillConfirmRequest,
    ) -> btrip_open_20220520_models.MonthBillConfirmResponse:
        """
        @summary 月账单确认
        
        @param request: MonthBillConfirmRequest
        @return: MonthBillConfirmResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.MonthBillConfirmHeaders()
        return await self.month_bill_confirm_with_options_async(request, headers, runtime)

    def month_bill_get_with_options(
        self,
        request: btrip_open_20220520_models.MonthBillGetRequest,
        headers: btrip_open_20220520_models.MonthBillGetHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.MonthBillGetResponse:
        """
        @summary 查询企业月账单
        
        @param request: MonthBillGetRequest
        @param headers: MonthBillGetHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: MonthBillGetResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.bill_month):
            query['bill_month'] = request.bill_month
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='MonthBillGet',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/open/v1/month-bill',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.MonthBillGetResponse(),
            self.call_api(params, req, runtime)
        )

    async def month_bill_get_with_options_async(
        self,
        request: btrip_open_20220520_models.MonthBillGetRequest,
        headers: btrip_open_20220520_models.MonthBillGetHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.MonthBillGetResponse:
        """
        @summary 查询企业月账单
        
        @param request: MonthBillGetRequest
        @param headers: MonthBillGetHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: MonthBillGetResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.bill_month):
            query['bill_month'] = request.bill_month
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='MonthBillGet',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/open/v1/month-bill',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.MonthBillGetResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def month_bill_get(
        self,
        request: btrip_open_20220520_models.MonthBillGetRequest,
    ) -> btrip_open_20220520_models.MonthBillGetResponse:
        """
        @summary 查询企业月账单
        
        @param request: MonthBillGetRequest
        @return: MonthBillGetResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.MonthBillGetHeaders()
        return self.month_bill_get_with_options(request, headers, runtime)

    async def month_bill_get_async(
        self,
        request: btrip_open_20220520_models.MonthBillGetRequest,
    ) -> btrip_open_20220520_models.MonthBillGetResponse:
        """
        @summary 查询企业月账单
        
        @param request: MonthBillGetRequest
        @return: MonthBillGetResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.MonthBillGetHeaders()
        return await self.month_bill_get_with_options_async(request, headers, runtime)

    def project_add_with_options(
        self,
        request: btrip_open_20220520_models.ProjectAddRequest,
        headers: btrip_open_20220520_models.ProjectAddHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.ProjectAddResponse:
        """
        @summary 添加项目
        
        @param request: ProjectAddRequest
        @param headers: ProjectAddHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: ProjectAddResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.code):
            body['code'] = request.code
        if not UtilClient.is_unset(request.project_name):
            body['project_name'] = request.project_name
        if not UtilClient.is_unset(request.third_part_cost_center_id):
            body['third_part_cost_center_id'] = request.third_part_cost_center_id
        if not UtilClient.is_unset(request.third_part_id):
            body['third_part_id'] = request.third_part_id
        if not UtilClient.is_unset(request.third_part_invoice_id):
            body['third_part_invoice_id'] = request.third_part_invoice_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='ProjectAdd',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/cost/v1/project',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.ProjectAddResponse(),
            self.call_api(params, req, runtime)
        )

    async def project_add_with_options_async(
        self,
        request: btrip_open_20220520_models.ProjectAddRequest,
        headers: btrip_open_20220520_models.ProjectAddHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.ProjectAddResponse:
        """
        @summary 添加项目
        
        @param request: ProjectAddRequest
        @param headers: ProjectAddHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: ProjectAddResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.code):
            body['code'] = request.code
        if not UtilClient.is_unset(request.project_name):
            body['project_name'] = request.project_name
        if not UtilClient.is_unset(request.third_part_cost_center_id):
            body['third_part_cost_center_id'] = request.third_part_cost_center_id
        if not UtilClient.is_unset(request.third_part_id):
            body['third_part_id'] = request.third_part_id
        if not UtilClient.is_unset(request.third_part_invoice_id):
            body['third_part_invoice_id'] = request.third_part_invoice_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='ProjectAdd',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/cost/v1/project',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.ProjectAddResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def project_add(
        self,
        request: btrip_open_20220520_models.ProjectAddRequest,
    ) -> btrip_open_20220520_models.ProjectAddResponse:
        """
        @summary 添加项目
        
        @param request: ProjectAddRequest
        @return: ProjectAddResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.ProjectAddHeaders()
        return self.project_add_with_options(request, headers, runtime)

    async def project_add_async(
        self,
        request: btrip_open_20220520_models.ProjectAddRequest,
    ) -> btrip_open_20220520_models.ProjectAddResponse:
        """
        @summary 添加项目
        
        @param request: ProjectAddRequest
        @return: ProjectAddResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.ProjectAddHeaders()
        return await self.project_add_with_options_async(request, headers, runtime)

    def project_delete_with_options(
        self,
        request: btrip_open_20220520_models.ProjectDeleteRequest,
        headers: btrip_open_20220520_models.ProjectDeleteHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.ProjectDeleteResponse:
        """
        @summary 删除项目
        
        @param request: ProjectDeleteRequest
        @param headers: ProjectDeleteHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: ProjectDeleteResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.third_part_id):
            query['third_part_id'] = request.third_part_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ProjectDelete',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/cost/v1/project',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.ProjectDeleteResponse(),
            self.call_api(params, req, runtime)
        )

    async def project_delete_with_options_async(
        self,
        request: btrip_open_20220520_models.ProjectDeleteRequest,
        headers: btrip_open_20220520_models.ProjectDeleteHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.ProjectDeleteResponse:
        """
        @summary 删除项目
        
        @param request: ProjectDeleteRequest
        @param headers: ProjectDeleteHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: ProjectDeleteResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.third_part_id):
            query['third_part_id'] = request.third_part_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='ProjectDelete',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/cost/v1/project',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.ProjectDeleteResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def project_delete(
        self,
        request: btrip_open_20220520_models.ProjectDeleteRequest,
    ) -> btrip_open_20220520_models.ProjectDeleteResponse:
        """
        @summary 删除项目
        
        @param request: ProjectDeleteRequest
        @return: ProjectDeleteResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.ProjectDeleteHeaders()
        return self.project_delete_with_options(request, headers, runtime)

    async def project_delete_async(
        self,
        request: btrip_open_20220520_models.ProjectDeleteRequest,
    ) -> btrip_open_20220520_models.ProjectDeleteResponse:
        """
        @summary 删除项目
        
        @param request: ProjectDeleteRequest
        @return: ProjectDeleteResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.ProjectDeleteHeaders()
        return await self.project_delete_with_options_async(request, headers, runtime)

    def project_modify_with_options(
        self,
        request: btrip_open_20220520_models.ProjectModifyRequest,
        headers: btrip_open_20220520_models.ProjectModifyHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.ProjectModifyResponse:
        """
        @summary 变更项目
        
        @param request: ProjectModifyRequest
        @param headers: ProjectModifyHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: ProjectModifyResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.code):
            body['code'] = request.code
        if not UtilClient.is_unset(request.project_name):
            body['project_name'] = request.project_name
        if not UtilClient.is_unset(request.third_part_cost_center_id):
            body['third_part_cost_center_id'] = request.third_part_cost_center_id
        if not UtilClient.is_unset(request.third_part_id):
            body['third_part_id'] = request.third_part_id
        if not UtilClient.is_unset(request.third_part_invoice_id):
            body['third_part_invoice_id'] = request.third_part_invoice_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='ProjectModify',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/cost/v1/project',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.ProjectModifyResponse(),
            self.call_api(params, req, runtime)
        )

    async def project_modify_with_options_async(
        self,
        request: btrip_open_20220520_models.ProjectModifyRequest,
        headers: btrip_open_20220520_models.ProjectModifyHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.ProjectModifyResponse:
        """
        @summary 变更项目
        
        @param request: ProjectModifyRequest
        @param headers: ProjectModifyHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: ProjectModifyResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.code):
            body['code'] = request.code
        if not UtilClient.is_unset(request.project_name):
            body['project_name'] = request.project_name
        if not UtilClient.is_unset(request.third_part_cost_center_id):
            body['third_part_cost_center_id'] = request.third_part_cost_center_id
        if not UtilClient.is_unset(request.third_part_id):
            body['third_part_id'] = request.third_part_id
        if not UtilClient.is_unset(request.third_part_invoice_id):
            body['third_part_invoice_id'] = request.third_part_invoice_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='ProjectModify',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/cost/v1/project',
            method='PUT',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.ProjectModifyResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def project_modify(
        self,
        request: btrip_open_20220520_models.ProjectModifyRequest,
    ) -> btrip_open_20220520_models.ProjectModifyResponse:
        """
        @summary 变更项目
        
        @param request: ProjectModifyRequest
        @return: ProjectModifyResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.ProjectModifyHeaders()
        return self.project_modify_with_options(request, headers, runtime)

    async def project_modify_async(
        self,
        request: btrip_open_20220520_models.ProjectModifyRequest,
    ) -> btrip_open_20220520_models.ProjectModifyResponse:
        """
        @summary 变更项目
        
        @param request: ProjectModifyRequest
        @return: ProjectModifyResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.ProjectModifyHeaders()
        return await self.project_modify_with_options_async(request, headers, runtime)

    def query_reimbursement_order_with_options(
        self,
        request: btrip_open_20220520_models.QueryReimbursementOrderRequest,
        headers: btrip_open_20220520_models.QueryReimbursementOrderHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.QueryReimbursementOrderResponse:
        """
        @summary 报销单查询
        
        @param request: QueryReimbursementOrderRequest
        @param headers: QueryReimbursementOrderHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: QueryReimbursementOrderResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.reimb_order_no):
            query['reimb_order_no'] = request.reimb_order_no
        if not UtilClient.is_unset(request.sub_corp_id):
            query['sub_corp_id'] = request.sub_corp_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='QueryReimbursementOrder',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/reimbursement/v1/order',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.QueryReimbursementOrderResponse(),
            self.call_api(params, req, runtime)
        )

    async def query_reimbursement_order_with_options_async(
        self,
        request: btrip_open_20220520_models.QueryReimbursementOrderRequest,
        headers: btrip_open_20220520_models.QueryReimbursementOrderHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.QueryReimbursementOrderResponse:
        """
        @summary 报销单查询
        
        @param request: QueryReimbursementOrderRequest
        @param headers: QueryReimbursementOrderHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: QueryReimbursementOrderResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.reimb_order_no):
            query['reimb_order_no'] = request.reimb_order_no
        if not UtilClient.is_unset(request.sub_corp_id):
            query['sub_corp_id'] = request.sub_corp_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='QueryReimbursementOrder',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/reimbursement/v1/order',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.QueryReimbursementOrderResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def query_reimbursement_order(
        self,
        request: btrip_open_20220520_models.QueryReimbursementOrderRequest,
    ) -> btrip_open_20220520_models.QueryReimbursementOrderResponse:
        """
        @summary 报销单查询
        
        @param request: QueryReimbursementOrderRequest
        @return: QueryReimbursementOrderResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.QueryReimbursementOrderHeaders()
        return self.query_reimbursement_order_with_options(request, headers, runtime)

    async def query_reimbursement_order_async(
        self,
        request: btrip_open_20220520_models.QueryReimbursementOrderRequest,
    ) -> btrip_open_20220520_models.QueryReimbursementOrderResponse:
        """
        @summary 报销单查询
        
        @param request: QueryReimbursementOrderRequest
        @return: QueryReimbursementOrderResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.QueryReimbursementOrderHeaders()
        return await self.query_reimbursement_order_with_options_async(request, headers, runtime)

    def sync_single_user_with_options(
        self,
        tmp_req: btrip_open_20220520_models.SyncSingleUserRequest,
        headers: btrip_open_20220520_models.SyncSingleUserHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.SyncSingleUserResponse:
        """
        @summary 单个人员同步
        
        @param tmp_req: SyncSingleUserRequest
        @param headers: SyncSingleUserHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: SyncSingleUserResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.SyncSingleUserShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.third_depart_id_list):
            request.third_depart_id_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.third_depart_id_list, 'third_depart_id_list', 'json')
        body = {}
        if not UtilClient.is_unset(request.email):
            body['email'] = request.email
        if not UtilClient.is_unset(request.job_no):
            body['job_no'] = request.job_no
        if not UtilClient.is_unset(request.leave_status):
            body['leave_status'] = request.leave_status
        if not UtilClient.is_unset(request.manager_user_id):
            body['manager_user_id'] = request.manager_user_id
        if not UtilClient.is_unset(request.phone):
            body['phone'] = request.phone
        if not UtilClient.is_unset(request.position):
            body['position'] = request.position
        if not UtilClient.is_unset(request.position_level):
            body['position_level'] = request.position_level
        if not UtilClient.is_unset(request.real_name_en):
            body['real_name_en'] = request.real_name_en
        if not UtilClient.is_unset(request.third_depart_id_list_shrink):
            body['third_depart_id_list'] = request.third_depart_id_list_shrink
        if not UtilClient.is_unset(request.user_id):
            body['user_id'] = request.user_id
        if not UtilClient.is_unset(request.user_name):
            body['user_name'] = request.user_name
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='SyncSingleUser',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/user/v1/single-user/action/sync',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.SyncSingleUserResponse(),
            self.call_api(params, req, runtime)
        )

    async def sync_single_user_with_options_async(
        self,
        tmp_req: btrip_open_20220520_models.SyncSingleUserRequest,
        headers: btrip_open_20220520_models.SyncSingleUserHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.SyncSingleUserResponse:
        """
        @summary 单个人员同步
        
        @param tmp_req: SyncSingleUserRequest
        @param headers: SyncSingleUserHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: SyncSingleUserResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.SyncSingleUserShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.third_depart_id_list):
            request.third_depart_id_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.third_depart_id_list, 'third_depart_id_list', 'json')
        body = {}
        if not UtilClient.is_unset(request.email):
            body['email'] = request.email
        if not UtilClient.is_unset(request.job_no):
            body['job_no'] = request.job_no
        if not UtilClient.is_unset(request.leave_status):
            body['leave_status'] = request.leave_status
        if not UtilClient.is_unset(request.manager_user_id):
            body['manager_user_id'] = request.manager_user_id
        if not UtilClient.is_unset(request.phone):
            body['phone'] = request.phone
        if not UtilClient.is_unset(request.position):
            body['position'] = request.position
        if not UtilClient.is_unset(request.position_level):
            body['position_level'] = request.position_level
        if not UtilClient.is_unset(request.real_name_en):
            body['real_name_en'] = request.real_name_en
        if not UtilClient.is_unset(request.third_depart_id_list_shrink):
            body['third_depart_id_list'] = request.third_depart_id_list_shrink
        if not UtilClient.is_unset(request.user_id):
            body['user_id'] = request.user_id
        if not UtilClient.is_unset(request.user_name):
            body['user_name'] = request.user_name
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='SyncSingleUser',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/user/v1/single-user/action/sync',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.SyncSingleUserResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def sync_single_user(
        self,
        request: btrip_open_20220520_models.SyncSingleUserRequest,
    ) -> btrip_open_20220520_models.SyncSingleUserResponse:
        """
        @summary 单个人员同步
        
        @param request: SyncSingleUserRequest
        @return: SyncSingleUserResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.SyncSingleUserHeaders()
        return self.sync_single_user_with_options(request, headers, runtime)

    async def sync_single_user_async(
        self,
        request: btrip_open_20220520_models.SyncSingleUserRequest,
    ) -> btrip_open_20220520_models.SyncSingleUserResponse:
        """
        @summary 单个人员同步
        
        @param request: SyncSingleUserRequest
        @return: SyncSingleUserResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.SyncSingleUserHeaders()
        return await self.sync_single_user_with_options_async(request, headers, runtime)

    def sync_third_user_mapping_with_options(
        self,
        request: btrip_open_20220520_models.SyncThirdUserMappingRequest,
        headers: btrip_open_20220520_models.SyncThirdUserMappingHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.SyncThirdUserMappingResponse:
        """
        @summary 同步三方用户映射关系
        
        @param request: SyncThirdUserMappingRequest
        @param headers: SyncThirdUserMappingHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: SyncThirdUserMappingResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.status):
            body['status'] = request.status
        if not UtilClient.is_unset(request.third_channel_type):
            body['third_channel_type'] = request.third_channel_type
        if not UtilClient.is_unset(request.third_user_id):
            body['third_user_id'] = request.third_user_id
        if not UtilClient.is_unset(request.user_id):
            body['user_id'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='SyncThirdUserMapping',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/user/v1/third-users/action/mapping',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.SyncThirdUserMappingResponse(),
            self.call_api(params, req, runtime)
        )

    async def sync_third_user_mapping_with_options_async(
        self,
        request: btrip_open_20220520_models.SyncThirdUserMappingRequest,
        headers: btrip_open_20220520_models.SyncThirdUserMappingHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.SyncThirdUserMappingResponse:
        """
        @summary 同步三方用户映射关系
        
        @param request: SyncThirdUserMappingRequest
        @param headers: SyncThirdUserMappingHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: SyncThirdUserMappingResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.status):
            body['status'] = request.status
        if not UtilClient.is_unset(request.third_channel_type):
            body['third_channel_type'] = request.third_channel_type
        if not UtilClient.is_unset(request.third_user_id):
            body['third_user_id'] = request.third_user_id
        if not UtilClient.is_unset(request.user_id):
            body['user_id'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='SyncThirdUserMapping',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/user/v1/third-users/action/mapping',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.SyncThirdUserMappingResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def sync_third_user_mapping(
        self,
        request: btrip_open_20220520_models.SyncThirdUserMappingRequest,
    ) -> btrip_open_20220520_models.SyncThirdUserMappingResponse:
        """
        @summary 同步三方用户映射关系
        
        @param request: SyncThirdUserMappingRequest
        @return: SyncThirdUserMappingResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.SyncThirdUserMappingHeaders()
        return self.sync_third_user_mapping_with_options(request, headers, runtime)

    async def sync_third_user_mapping_async(
        self,
        request: btrip_open_20220520_models.SyncThirdUserMappingRequest,
    ) -> btrip_open_20220520_models.SyncThirdUserMappingResponse:
        """
        @summary 同步三方用户映射关系
        
        @param request: SyncThirdUserMappingRequest
        @return: SyncThirdUserMappingResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.SyncThirdUserMappingHeaders()
        return await self.sync_third_user_mapping_with_options_async(request, headers, runtime)

    def t_baccount_info_query_with_options(
        self,
        user_id: str,
        headers: btrip_open_20220520_models.TBAccountInfoQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.TBAccountInfoQueryResponse:
        """
        @summary 查询淘宝账号信息
        
        @param headers: TBAccountInfoQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: TBAccountInfoQueryResponse
        """
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers
        )
        params = open_api_models.Params(
            action='TBAccountInfoQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/account/v1/tb-accounts/{OpenApiUtilClient.get_encode_param(user_id)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.TBAccountInfoQueryResponse(),
            self.call_api(params, req, runtime)
        )

    async def t_baccount_info_query_with_options_async(
        self,
        user_id: str,
        headers: btrip_open_20220520_models.TBAccountInfoQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.TBAccountInfoQueryResponse:
        """
        @summary 查询淘宝账号信息
        
        @param headers: TBAccountInfoQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: TBAccountInfoQueryResponse
        """
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers
        )
        params = open_api_models.Params(
            action='TBAccountInfoQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/account/v1/tb-accounts/{OpenApiUtilClient.get_encode_param(user_id)}',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.TBAccountInfoQueryResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def t_baccount_info_query(
        self,
        user_id: str,
    ) -> btrip_open_20220520_models.TBAccountInfoQueryResponse:
        """
        @summary 查询淘宝账号信息
        
        @return: TBAccountInfoQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.TBAccountInfoQueryHeaders()
        return self.t_baccount_info_query_with_options(user_id, headers, runtime)

    async def t_baccount_info_query_async(
        self,
        user_id: str,
    ) -> btrip_open_20220520_models.TBAccountInfoQueryResponse:
        """
        @summary 查询淘宝账号信息
        
        @return: TBAccountInfoQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.TBAccountInfoQueryHeaders()
        return await self.t_baccount_info_query_with_options_async(user_id, headers, runtime)

    def t_baccount_unbind_with_options(
        self,
        user_id: str,
        headers: btrip_open_20220520_models.TBAccountUnbindHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.TBAccountUnbindResponse:
        """
        @summary 解绑淘宝账号
        
        @param headers: TBAccountUnbindHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: TBAccountUnbindResponse
        """
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers
        )
        params = open_api_models.Params(
            action='TBAccountUnbind',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/account/v1/tb-accounts/{OpenApiUtilClient.get_encode_param(user_id)}/action/unbind',
            method='PATCH',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.TBAccountUnbindResponse(),
            self.call_api(params, req, runtime)
        )

    async def t_baccount_unbind_with_options_async(
        self,
        user_id: str,
        headers: btrip_open_20220520_models.TBAccountUnbindHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.TBAccountUnbindResponse:
        """
        @summary 解绑淘宝账号
        
        @param headers: TBAccountUnbindHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: TBAccountUnbindResponse
        """
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers
        )
        params = open_api_models.Params(
            action='TBAccountUnbind',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/account/v1/tb-accounts/{OpenApiUtilClient.get_encode_param(user_id)}/action/unbind',
            method='PATCH',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.TBAccountUnbindResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def t_baccount_unbind(
        self,
        user_id: str,
    ) -> btrip_open_20220520_models.TBAccountUnbindResponse:
        """
        @summary 解绑淘宝账号
        
        @return: TBAccountUnbindResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.TBAccountUnbindHeaders()
        return self.t_baccount_unbind_with_options(user_id, headers, runtime)

    async def t_baccount_unbind_async(
        self,
        user_id: str,
    ) -> btrip_open_20220520_models.TBAccountUnbindResponse:
        """
        @summary 解绑淘宝账号
        
        @return: TBAccountUnbindResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.TBAccountUnbindHeaders()
        return await self.t_baccount_unbind_with_options_async(user_id, headers, runtime)

    def ticket_changing_apply_with_options(
        self,
        tmp_req: btrip_open_20220520_models.TicketChangingApplyRequest,
        headers: btrip_open_20220520_models.TicketChangingApplyHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.TicketChangingApplyResponse:
        """
        @summary 机票改签申请
        
        @param tmp_req: TicketChangingApplyRequest
        @param headers: TicketChangingApplyHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: TicketChangingApplyResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.TicketChangingApplyShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.modify_flight_info_list):
            request.modify_flight_info_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.modify_flight_info_list, 'modify_flight_info_list', 'json')
        body = {}
        if not UtilClient.is_unset(request.dis_order_id):
            body['dis_order_id'] = request.dis_order_id
        if not UtilClient.is_unset(request.dis_sub_order_id):
            body['dis_sub_order_id'] = request.dis_sub_order_id
        if not UtilClient.is_unset(request.is_voluntary):
            body['is_voluntary'] = request.is_voluntary
        if not UtilClient.is_unset(request.modify_flight_info_list_shrink):
            body['modify_flight_info_list'] = request.modify_flight_info_list_shrink
        if not UtilClient.is_unset(request.ota_item_id):
            body['ota_item_id'] = request.ota_item_id
        if not UtilClient.is_unset(request.reason):
            body['reason'] = request.reason
        if not UtilClient.is_unset(request.session_id):
            body['session_id'] = request.session_id
        if not UtilClient.is_unset(request.whether_retry):
            body['whether_retry'] = request.whether_retry
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='TicketChangingApply',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v1/ticket-changing/action/apply',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.TicketChangingApplyResponse(),
            self.call_api(params, req, runtime)
        )

    async def ticket_changing_apply_with_options_async(
        self,
        tmp_req: btrip_open_20220520_models.TicketChangingApplyRequest,
        headers: btrip_open_20220520_models.TicketChangingApplyHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.TicketChangingApplyResponse:
        """
        @summary 机票改签申请
        
        @param tmp_req: TicketChangingApplyRequest
        @param headers: TicketChangingApplyHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: TicketChangingApplyResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.TicketChangingApplyShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.modify_flight_info_list):
            request.modify_flight_info_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.modify_flight_info_list, 'modify_flight_info_list', 'json')
        body = {}
        if not UtilClient.is_unset(request.dis_order_id):
            body['dis_order_id'] = request.dis_order_id
        if not UtilClient.is_unset(request.dis_sub_order_id):
            body['dis_sub_order_id'] = request.dis_sub_order_id
        if not UtilClient.is_unset(request.is_voluntary):
            body['is_voluntary'] = request.is_voluntary
        if not UtilClient.is_unset(request.modify_flight_info_list_shrink):
            body['modify_flight_info_list'] = request.modify_flight_info_list_shrink
        if not UtilClient.is_unset(request.ota_item_id):
            body['ota_item_id'] = request.ota_item_id
        if not UtilClient.is_unset(request.reason):
            body['reason'] = request.reason
        if not UtilClient.is_unset(request.session_id):
            body['session_id'] = request.session_id
        if not UtilClient.is_unset(request.whether_retry):
            body['whether_retry'] = request.whether_retry
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='TicketChangingApply',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v1/ticket-changing/action/apply',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.TicketChangingApplyResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def ticket_changing_apply(
        self,
        request: btrip_open_20220520_models.TicketChangingApplyRequest,
    ) -> btrip_open_20220520_models.TicketChangingApplyResponse:
        """
        @summary 机票改签申请
        
        @param request: TicketChangingApplyRequest
        @return: TicketChangingApplyResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.TicketChangingApplyHeaders()
        return self.ticket_changing_apply_with_options(request, headers, runtime)

    async def ticket_changing_apply_async(
        self,
        request: btrip_open_20220520_models.TicketChangingApplyRequest,
    ) -> btrip_open_20220520_models.TicketChangingApplyResponse:
        """
        @summary 机票改签申请
        
        @param request: TicketChangingApplyRequest
        @return: TicketChangingApplyResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.TicketChangingApplyHeaders()
        return await self.ticket_changing_apply_with_options_async(request, headers, runtime)

    def ticket_changing_cancel_with_options(
        self,
        request: btrip_open_20220520_models.TicketChangingCancelRequest,
        headers: btrip_open_20220520_models.TicketChangingCancelHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.TicketChangingCancelResponse:
        """
        @summary 机票改签取消
        
        @param request: TicketChangingCancelRequest
        @param headers: TicketChangingCancelHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: TicketChangingCancelResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.dis_order_id):
            query['dis_order_id'] = request.dis_order_id
        if not UtilClient.is_unset(request.dis_sub_order_id):
            query['dis_sub_order_id'] = request.dis_sub_order_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='TicketChangingCancel',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v1/ticket-changing/action/cancel',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.TicketChangingCancelResponse(),
            self.call_api(params, req, runtime)
        )

    async def ticket_changing_cancel_with_options_async(
        self,
        request: btrip_open_20220520_models.TicketChangingCancelRequest,
        headers: btrip_open_20220520_models.TicketChangingCancelHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.TicketChangingCancelResponse:
        """
        @summary 机票改签取消
        
        @param request: TicketChangingCancelRequest
        @param headers: TicketChangingCancelHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: TicketChangingCancelResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.dis_order_id):
            query['dis_order_id'] = request.dis_order_id
        if not UtilClient.is_unset(request.dis_sub_order_id):
            query['dis_sub_order_id'] = request.dis_sub_order_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='TicketChangingCancel',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v1/ticket-changing/action/cancel',
            method='DELETE',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.TicketChangingCancelResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def ticket_changing_cancel(
        self,
        request: btrip_open_20220520_models.TicketChangingCancelRequest,
    ) -> btrip_open_20220520_models.TicketChangingCancelResponse:
        """
        @summary 机票改签取消
        
        @param request: TicketChangingCancelRequest
        @return: TicketChangingCancelResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.TicketChangingCancelHeaders()
        return self.ticket_changing_cancel_with_options(request, headers, runtime)

    async def ticket_changing_cancel_async(
        self,
        request: btrip_open_20220520_models.TicketChangingCancelRequest,
    ) -> btrip_open_20220520_models.TicketChangingCancelResponse:
        """
        @summary 机票改签取消
        
        @param request: TicketChangingCancelRequest
        @return: TicketChangingCancelResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.TicketChangingCancelHeaders()
        return await self.ticket_changing_cancel_with_options_async(request, headers, runtime)

    def ticket_changing_detail_with_options(
        self,
        request: btrip_open_20220520_models.TicketChangingDetailRequest,
        headers: btrip_open_20220520_models.TicketChangingDetailHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.TicketChangingDetailResponse:
        """
        @summary 机票改签详情
        
        @param request: TicketChangingDetailRequest
        @param headers: TicketChangingDetailHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: TicketChangingDetailResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.dis_order_id):
            query['dis_order_id'] = request.dis_order_id
        if not UtilClient.is_unset(request.dis_sub_order_id):
            query['dis_sub_order_id'] = request.dis_sub_order_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='TicketChangingDetail',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v1/ticket-changing/action/detail',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.TicketChangingDetailResponse(),
            self.call_api(params, req, runtime)
        )

    async def ticket_changing_detail_with_options_async(
        self,
        request: btrip_open_20220520_models.TicketChangingDetailRequest,
        headers: btrip_open_20220520_models.TicketChangingDetailHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.TicketChangingDetailResponse:
        """
        @summary 机票改签详情
        
        @param request: TicketChangingDetailRequest
        @param headers: TicketChangingDetailHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: TicketChangingDetailResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.dis_order_id):
            query['dis_order_id'] = request.dis_order_id
        if not UtilClient.is_unset(request.dis_sub_order_id):
            query['dis_sub_order_id'] = request.dis_sub_order_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='TicketChangingDetail',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v1/ticket-changing/action/detail',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.TicketChangingDetailResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def ticket_changing_detail(
        self,
        request: btrip_open_20220520_models.TicketChangingDetailRequest,
    ) -> btrip_open_20220520_models.TicketChangingDetailResponse:
        """
        @summary 机票改签详情
        
        @param request: TicketChangingDetailRequest
        @return: TicketChangingDetailResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.TicketChangingDetailHeaders()
        return self.ticket_changing_detail_with_options(request, headers, runtime)

    async def ticket_changing_detail_async(
        self,
        request: btrip_open_20220520_models.TicketChangingDetailRequest,
    ) -> btrip_open_20220520_models.TicketChangingDetailResponse:
        """
        @summary 机票改签详情
        
        @param request: TicketChangingDetailRequest
        @return: TicketChangingDetailResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.TicketChangingDetailHeaders()
        return await self.ticket_changing_detail_with_options_async(request, headers, runtime)

    def ticket_changing_enquiry_with_options(
        self,
        request: btrip_open_20220520_models.TicketChangingEnquiryRequest,
        headers: btrip_open_20220520_models.TicketChangingEnquiryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.TicketChangingEnquiryResponse:
        """
        @summary 机票改签询价
        
        @param request: TicketChangingEnquiryRequest
        @param headers: TicketChangingEnquiryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: TicketChangingEnquiryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.arr_city):
            query['arr_city'] = request.arr_city
        if not UtilClient.is_unset(request.dep_city):
            query['dep_city'] = request.dep_city
        if not UtilClient.is_unset(request.dis_order_id):
            query['dis_order_id'] = request.dis_order_id
        if not UtilClient.is_unset(request.is_voluntary):
            query['is_voluntary'] = request.is_voluntary
        if not UtilClient.is_unset(request.modify_depart_date):
            query['modify_depart_date'] = request.modify_depart_date
        if not UtilClient.is_unset(request.modify_flight_no):
            query['modify_flight_no'] = request.modify_flight_no
        if not UtilClient.is_unset(request.session_id):
            query['session_id'] = request.session_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='TicketChangingEnquiry',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v1/ticket-changing/action/enquiry',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.TicketChangingEnquiryResponse(),
            self.call_api(params, req, runtime)
        )

    async def ticket_changing_enquiry_with_options_async(
        self,
        request: btrip_open_20220520_models.TicketChangingEnquiryRequest,
        headers: btrip_open_20220520_models.TicketChangingEnquiryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.TicketChangingEnquiryResponse:
        """
        @summary 机票改签询价
        
        @param request: TicketChangingEnquiryRequest
        @param headers: TicketChangingEnquiryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: TicketChangingEnquiryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.arr_city):
            query['arr_city'] = request.arr_city
        if not UtilClient.is_unset(request.dep_city):
            query['dep_city'] = request.dep_city
        if not UtilClient.is_unset(request.dis_order_id):
            query['dis_order_id'] = request.dis_order_id
        if not UtilClient.is_unset(request.is_voluntary):
            query['is_voluntary'] = request.is_voluntary
        if not UtilClient.is_unset(request.modify_depart_date):
            query['modify_depart_date'] = request.modify_depart_date
        if not UtilClient.is_unset(request.modify_flight_no):
            query['modify_flight_no'] = request.modify_flight_no
        if not UtilClient.is_unset(request.session_id):
            query['session_id'] = request.session_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='TicketChangingEnquiry',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v1/ticket-changing/action/enquiry',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.TicketChangingEnquiryResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def ticket_changing_enquiry(
        self,
        request: btrip_open_20220520_models.TicketChangingEnquiryRequest,
    ) -> btrip_open_20220520_models.TicketChangingEnquiryResponse:
        """
        @summary 机票改签询价
        
        @param request: TicketChangingEnquiryRequest
        @return: TicketChangingEnquiryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.TicketChangingEnquiryHeaders()
        return self.ticket_changing_enquiry_with_options(request, headers, runtime)

    async def ticket_changing_enquiry_async(
        self,
        request: btrip_open_20220520_models.TicketChangingEnquiryRequest,
    ) -> btrip_open_20220520_models.TicketChangingEnquiryResponse:
        """
        @summary 机票改签询价
        
        @param request: TicketChangingEnquiryRequest
        @return: TicketChangingEnquiryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.TicketChangingEnquiryHeaders()
        return await self.ticket_changing_enquiry_with_options_async(request, headers, runtime)

    def ticket_changing_flight_list_with_options(
        self,
        tmp_req: btrip_open_20220520_models.TicketChangingFlightListRequest,
        headers: btrip_open_20220520_models.TicketChangingFlightListHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.TicketChangingFlightListResponse:
        """
        @summary 机票改签可改签航班列表
        
        @param tmp_req: TicketChangingFlightListRequest
        @param headers: TicketChangingFlightListHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: TicketChangingFlightListResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.TicketChangingFlightListShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.traveler_info_list):
            request.traveler_info_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.traveler_info_list, 'traveler_info_list', 'json')
        query = {}
        if not UtilClient.is_unset(request.arr_city):
            query['arr_city'] = request.arr_city
        if not UtilClient.is_unset(request.dep_city):
            query['dep_city'] = request.dep_city
        if not UtilClient.is_unset(request.dep_date):
            query['dep_date'] = request.dep_date
        if not UtilClient.is_unset(request.dis_order_id):
            query['dis_order_id'] = request.dis_order_id
        if not UtilClient.is_unset(request.is_voluntary):
            query['is_voluntary'] = request.is_voluntary
        if not UtilClient.is_unset(request.traveler_info_list_shrink):
            query['traveler_info_list'] = request.traveler_info_list_shrink
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='TicketChangingFlightList',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/huge/dtb-flight/v1/ticket-changing-flight/action/list',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.TicketChangingFlightListResponse(),
            self.call_api(params, req, runtime)
        )

    async def ticket_changing_flight_list_with_options_async(
        self,
        tmp_req: btrip_open_20220520_models.TicketChangingFlightListRequest,
        headers: btrip_open_20220520_models.TicketChangingFlightListHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.TicketChangingFlightListResponse:
        """
        @summary 机票改签可改签航班列表
        
        @param tmp_req: TicketChangingFlightListRequest
        @param headers: TicketChangingFlightListHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: TicketChangingFlightListResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.TicketChangingFlightListShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.traveler_info_list):
            request.traveler_info_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.traveler_info_list, 'traveler_info_list', 'json')
        query = {}
        if not UtilClient.is_unset(request.arr_city):
            query['arr_city'] = request.arr_city
        if not UtilClient.is_unset(request.dep_city):
            query['dep_city'] = request.dep_city
        if not UtilClient.is_unset(request.dep_date):
            query['dep_date'] = request.dep_date
        if not UtilClient.is_unset(request.dis_order_id):
            query['dis_order_id'] = request.dis_order_id
        if not UtilClient.is_unset(request.is_voluntary):
            query['is_voluntary'] = request.is_voluntary
        if not UtilClient.is_unset(request.traveler_info_list_shrink):
            query['traveler_info_list'] = request.traveler_info_list_shrink
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='TicketChangingFlightList',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/huge/dtb-flight/v1/ticket-changing-flight/action/list',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.TicketChangingFlightListResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def ticket_changing_flight_list(
        self,
        request: btrip_open_20220520_models.TicketChangingFlightListRequest,
    ) -> btrip_open_20220520_models.TicketChangingFlightListResponse:
        """
        @summary 机票改签可改签航班列表
        
        @param request: TicketChangingFlightListRequest
        @return: TicketChangingFlightListResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.TicketChangingFlightListHeaders()
        return self.ticket_changing_flight_list_with_options(request, headers, runtime)

    async def ticket_changing_flight_list_async(
        self,
        request: btrip_open_20220520_models.TicketChangingFlightListRequest,
    ) -> btrip_open_20220520_models.TicketChangingFlightListResponse:
        """
        @summary 机票改签可改签航班列表
        
        @param request: TicketChangingFlightListRequest
        @return: TicketChangingFlightListResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.TicketChangingFlightListHeaders()
        return await self.ticket_changing_flight_list_with_options_async(request, headers, runtime)

    def ticket_changing_pay_with_options(
        self,
        tmp_req: btrip_open_20220520_models.TicketChangingPayRequest,
        headers: btrip_open_20220520_models.TicketChangingPayHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.TicketChangingPayResponse:
        """
        @summary 机票改签航班支付
        
        @param tmp_req: TicketChangingPayRequest
        @param headers: TicketChangingPayHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: TicketChangingPayResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.TicketChangingPayShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.extra):
            request.extra_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.extra, 'extra', 'json')
        body = {}
        if not UtilClient.is_unset(request.corp_pay_price):
            body['corp_pay_price'] = request.corp_pay_price
        if not UtilClient.is_unset(request.dis_order_id):
            body['dis_order_id'] = request.dis_order_id
        if not UtilClient.is_unset(request.dis_sub_order_id):
            body['dis_sub_order_id'] = request.dis_sub_order_id
        if not UtilClient.is_unset(request.extra_shrink):
            body['extra'] = request.extra_shrink
        if not UtilClient.is_unset(request.personal_pay_price):
            body['personal_pay_price'] = request.personal_pay_price
        if not UtilClient.is_unset(request.total_pay_price):
            body['total_pay_price'] = request.total_pay_price
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='TicketChangingPay',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v1/ticket-changing/action/pay',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.TicketChangingPayResponse(),
            self.call_api(params, req, runtime)
        )

    async def ticket_changing_pay_with_options_async(
        self,
        tmp_req: btrip_open_20220520_models.TicketChangingPayRequest,
        headers: btrip_open_20220520_models.TicketChangingPayHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.TicketChangingPayResponse:
        """
        @summary 机票改签航班支付
        
        @param tmp_req: TicketChangingPayRequest
        @param headers: TicketChangingPayHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: TicketChangingPayResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.TicketChangingPayShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.extra):
            request.extra_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.extra, 'extra', 'json')
        body = {}
        if not UtilClient.is_unset(request.corp_pay_price):
            body['corp_pay_price'] = request.corp_pay_price
        if not UtilClient.is_unset(request.dis_order_id):
            body['dis_order_id'] = request.dis_order_id
        if not UtilClient.is_unset(request.dis_sub_order_id):
            body['dis_sub_order_id'] = request.dis_sub_order_id
        if not UtilClient.is_unset(request.extra_shrink):
            body['extra'] = request.extra_shrink
        if not UtilClient.is_unset(request.personal_pay_price):
            body['personal_pay_price'] = request.personal_pay_price
        if not UtilClient.is_unset(request.total_pay_price):
            body['total_pay_price'] = request.total_pay_price
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='TicketChangingPay',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/dtb-flight/v1/ticket-changing/action/pay',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.TicketChangingPayResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def ticket_changing_pay(
        self,
        request: btrip_open_20220520_models.TicketChangingPayRequest,
    ) -> btrip_open_20220520_models.TicketChangingPayResponse:
        """
        @summary 机票改签航班支付
        
        @param request: TicketChangingPayRequest
        @return: TicketChangingPayResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.TicketChangingPayHeaders()
        return self.ticket_changing_pay_with_options(request, headers, runtime)

    async def ticket_changing_pay_async(
        self,
        request: btrip_open_20220520_models.TicketChangingPayRequest,
    ) -> btrip_open_20220520_models.TicketChangingPayResponse:
        """
        @summary 机票改签航班支付
        
        @param request: TicketChangingPayRequest
        @return: TicketChangingPayResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.TicketChangingPayHeaders()
        return await self.ticket_changing_pay_with_options_async(request, headers, runtime)

    def train_apply_change_with_options(
        self,
        tmp_req: btrip_open_20220520_models.TrainApplyChangeRequest,
        headers: btrip_open_20220520_models.TrainApplyChangeHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.TrainApplyChangeResponse:
        """
        @summary 火车票改签申请
        
        @param tmp_req: TrainApplyChangeRequest
        @param headers: TrainApplyChangeHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: TrainApplyChangeResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.TrainApplyChangeShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.change_train_info_s):
            request.change_train_info_sshrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.change_train_info_s, 'change_train_info_s', 'json')
        query = {}
        if not UtilClient.is_unset(request.change_train_info_sshrink):
            query['change_train_info_s'] = request.change_train_info_sshrink
        body = {}
        if not UtilClient.is_unset(request.accept_no_seat):
            body['accept_no_seat'] = request.accept_no_seat
        if not UtilClient.is_unset(request.force_match):
            body['force_match'] = request.force_match
        if not UtilClient.is_unset(request.is_pay_now):
            body['is_pay_now'] = request.is_pay_now
        if not UtilClient.is_unset(request.order_id):
            body['order_id'] = request.order_id
        if not UtilClient.is_unset(request.out_change_apply_id):
            body['out_change_apply_id'] = request.out_change_apply_id
        if not UtilClient.is_unset(request.out_order_id):
            body['out_order_id'] = request.out_order_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='TrainApplyChange',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/train/v1/change/apply',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.TrainApplyChangeResponse(),
            self.call_api(params, req, runtime)
        )

    async def train_apply_change_with_options_async(
        self,
        tmp_req: btrip_open_20220520_models.TrainApplyChangeRequest,
        headers: btrip_open_20220520_models.TrainApplyChangeHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.TrainApplyChangeResponse:
        """
        @summary 火车票改签申请
        
        @param tmp_req: TrainApplyChangeRequest
        @param headers: TrainApplyChangeHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: TrainApplyChangeResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.TrainApplyChangeShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.change_train_info_s):
            request.change_train_info_sshrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.change_train_info_s, 'change_train_info_s', 'json')
        query = {}
        if not UtilClient.is_unset(request.change_train_info_sshrink):
            query['change_train_info_s'] = request.change_train_info_sshrink
        body = {}
        if not UtilClient.is_unset(request.accept_no_seat):
            body['accept_no_seat'] = request.accept_no_seat
        if not UtilClient.is_unset(request.force_match):
            body['force_match'] = request.force_match
        if not UtilClient.is_unset(request.is_pay_now):
            body['is_pay_now'] = request.is_pay_now
        if not UtilClient.is_unset(request.order_id):
            body['order_id'] = request.order_id
        if not UtilClient.is_unset(request.out_change_apply_id):
            body['out_change_apply_id'] = request.out_change_apply_id
        if not UtilClient.is_unset(request.out_order_id):
            body['out_order_id'] = request.out_order_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query),
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='TrainApplyChange',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/train/v1/change/apply',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.TrainApplyChangeResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def train_apply_change(
        self,
        request: btrip_open_20220520_models.TrainApplyChangeRequest,
    ) -> btrip_open_20220520_models.TrainApplyChangeResponse:
        """
        @summary 火车票改签申请
        
        @param request: TrainApplyChangeRequest
        @return: TrainApplyChangeResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.TrainApplyChangeHeaders()
        return self.train_apply_change_with_options(request, headers, runtime)

    async def train_apply_change_async(
        self,
        request: btrip_open_20220520_models.TrainApplyChangeRequest,
    ) -> btrip_open_20220520_models.TrainApplyChangeResponse:
        """
        @summary 火车票改签申请
        
        @param request: TrainApplyChangeRequest
        @return: TrainApplyChangeResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.TrainApplyChangeHeaders()
        return await self.train_apply_change_with_options_async(request, headers, runtime)

    def train_apply_refund_with_options(
        self,
        tmp_req: btrip_open_20220520_models.TrainApplyRefundRequest,
        headers: btrip_open_20220520_models.TrainApplyRefundHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.TrainApplyRefundResponse:
        """
        @summary 火车票退票申请
        
        @param tmp_req: TrainApplyRefundRequest
        @param headers: TrainApplyRefundHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: TrainApplyRefundResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.TrainApplyRefundShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.refund_train_infos):
            request.refund_train_infos_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.refund_train_infos, 'refund_train_infos', 'json')
        body = {}
        if not UtilClient.is_unset(request.order_id):
            body['order_id'] = request.order_id
        if not UtilClient.is_unset(request.out_order_id):
            body['out_order_id'] = request.out_order_id
        if not UtilClient.is_unset(request.out_refund_id):
            body['out_refund_id'] = request.out_refund_id
        if not UtilClient.is_unset(request.refund_train_infos_shrink):
            body['refund_train_infos'] = request.refund_train_infos_shrink
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='TrainApplyRefund',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/train/v1/refund/apply',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.TrainApplyRefundResponse(),
            self.call_api(params, req, runtime)
        )

    async def train_apply_refund_with_options_async(
        self,
        tmp_req: btrip_open_20220520_models.TrainApplyRefundRequest,
        headers: btrip_open_20220520_models.TrainApplyRefundHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.TrainApplyRefundResponse:
        """
        @summary 火车票退票申请
        
        @param tmp_req: TrainApplyRefundRequest
        @param headers: TrainApplyRefundHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: TrainApplyRefundResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.TrainApplyRefundShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.refund_train_infos):
            request.refund_train_infos_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.refund_train_infos, 'refund_train_infos', 'json')
        body = {}
        if not UtilClient.is_unset(request.order_id):
            body['order_id'] = request.order_id
        if not UtilClient.is_unset(request.out_order_id):
            body['out_order_id'] = request.out_order_id
        if not UtilClient.is_unset(request.out_refund_id):
            body['out_refund_id'] = request.out_refund_id
        if not UtilClient.is_unset(request.refund_train_infos_shrink):
            body['refund_train_infos'] = request.refund_train_infos_shrink
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='TrainApplyRefund',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/train/v1/refund/apply',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.TrainApplyRefundResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def train_apply_refund(
        self,
        request: btrip_open_20220520_models.TrainApplyRefundRequest,
    ) -> btrip_open_20220520_models.TrainApplyRefundResponse:
        """
        @summary 火车票退票申请
        
        @param request: TrainApplyRefundRequest
        @return: TrainApplyRefundResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.TrainApplyRefundHeaders()
        return self.train_apply_refund_with_options(request, headers, runtime)

    async def train_apply_refund_async(
        self,
        request: btrip_open_20220520_models.TrainApplyRefundRequest,
    ) -> btrip_open_20220520_models.TrainApplyRefundResponse:
        """
        @summary 火车票退票申请
        
        @param request: TrainApplyRefundRequest
        @return: TrainApplyRefundResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.TrainApplyRefundHeaders()
        return await self.train_apply_refund_with_options_async(request, headers, runtime)

    def train_bill_settlement_query_with_options(
        self,
        request: btrip_open_20220520_models.TrainBillSettlementQueryRequest,
        headers: btrip_open_20220520_models.TrainBillSettlementQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.TrainBillSettlementQueryResponse:
        """
        @summary 查询火车票记账数据
        
        @param request: TrainBillSettlementQueryRequest
        @param headers: TrainBillSettlementQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: TrainBillSettlementQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.page_no):
            query['page_no'] = request.page_no
        if not UtilClient.is_unset(request.page_size):
            query['page_size'] = request.page_size
        if not UtilClient.is_unset(request.period_end):
            query['period_end'] = request.period_end
        if not UtilClient.is_unset(request.period_start):
            query['period_start'] = request.period_start
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='TrainBillSettlementQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/train/v1/bill-settlement',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.TrainBillSettlementQueryResponse(),
            self.call_api(params, req, runtime)
        )

    async def train_bill_settlement_query_with_options_async(
        self,
        request: btrip_open_20220520_models.TrainBillSettlementQueryRequest,
        headers: btrip_open_20220520_models.TrainBillSettlementQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.TrainBillSettlementQueryResponse:
        """
        @summary 查询火车票记账数据
        
        @param request: TrainBillSettlementQueryRequest
        @param headers: TrainBillSettlementQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: TrainBillSettlementQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.page_no):
            query['page_no'] = request.page_no
        if not UtilClient.is_unset(request.page_size):
            query['page_size'] = request.page_size
        if not UtilClient.is_unset(request.period_end):
            query['period_end'] = request.period_end
        if not UtilClient.is_unset(request.period_start):
            query['period_start'] = request.period_start
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='TrainBillSettlementQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/train/v1/bill-settlement',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.TrainBillSettlementQueryResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def train_bill_settlement_query(
        self,
        request: btrip_open_20220520_models.TrainBillSettlementQueryRequest,
    ) -> btrip_open_20220520_models.TrainBillSettlementQueryResponse:
        """
        @summary 查询火车票记账数据
        
        @param request: TrainBillSettlementQueryRequest
        @return: TrainBillSettlementQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.TrainBillSettlementQueryHeaders()
        return self.train_bill_settlement_query_with_options(request, headers, runtime)

    async def train_bill_settlement_query_async(
        self,
        request: btrip_open_20220520_models.TrainBillSettlementQueryRequest,
    ) -> btrip_open_20220520_models.TrainBillSettlementQueryResponse:
        """
        @summary 查询火车票记账数据
        
        @param request: TrainBillSettlementQueryRequest
        @return: TrainBillSettlementQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.TrainBillSettlementQueryHeaders()
        return await self.train_bill_settlement_query_with_options_async(request, headers, runtime)

    def train_exceed_apply_query_with_options(
        self,
        request: btrip_open_20220520_models.TrainExceedApplyQueryRequest,
        headers: btrip_open_20220520_models.TrainExceedApplyQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.TrainExceedApplyQueryResponse:
        """
        @summary 查询火车超标审批详情
        
        @param request: TrainExceedApplyQueryRequest
        @param headers: TrainExceedApplyQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: TrainExceedApplyQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.apply_id):
            query['apply_id'] = request.apply_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='TrainExceedApplyQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/apply/v1/train-exceed',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.TrainExceedApplyQueryResponse(),
            self.call_api(params, req, runtime)
        )

    async def train_exceed_apply_query_with_options_async(
        self,
        request: btrip_open_20220520_models.TrainExceedApplyQueryRequest,
        headers: btrip_open_20220520_models.TrainExceedApplyQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.TrainExceedApplyQueryResponse:
        """
        @summary 查询火车超标审批详情
        
        @param request: TrainExceedApplyQueryRequest
        @param headers: TrainExceedApplyQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: TrainExceedApplyQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.apply_id):
            query['apply_id'] = request.apply_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='TrainExceedApplyQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/apply/v1/train-exceed',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.TrainExceedApplyQueryResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def train_exceed_apply_query(
        self,
        request: btrip_open_20220520_models.TrainExceedApplyQueryRequest,
    ) -> btrip_open_20220520_models.TrainExceedApplyQueryResponse:
        """
        @summary 查询火车超标审批详情
        
        @param request: TrainExceedApplyQueryRequest
        @return: TrainExceedApplyQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.TrainExceedApplyQueryHeaders()
        return self.train_exceed_apply_query_with_options(request, headers, runtime)

    async def train_exceed_apply_query_async(
        self,
        request: btrip_open_20220520_models.TrainExceedApplyQueryRequest,
    ) -> btrip_open_20220520_models.TrainExceedApplyQueryResponse:
        """
        @summary 查询火车超标审批详情
        
        @param request: TrainExceedApplyQueryRequest
        @return: TrainExceedApplyQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.TrainExceedApplyQueryHeaders()
        return await self.train_exceed_apply_query_with_options_async(request, headers, runtime)

    def train_fee_calculate_change_with_options(
        self,
        tmp_req: btrip_open_20220520_models.TrainFeeCalculateChangeRequest,
        headers: btrip_open_20220520_models.TrainFeeCalculateChangeHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.TrainFeeCalculateChangeResponse:
        """
        @summary 火车票改签费用预估
        
        @param tmp_req: TrainFeeCalculateChangeRequest
        @param headers: TrainFeeCalculateChangeHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: TrainFeeCalculateChangeResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.TrainFeeCalculateChangeShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.change_train_details):
            request.change_train_details_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.change_train_details, 'change_train_details', 'json')
        body = {}
        if not UtilClient.is_unset(request.change_train_details_shrink):
            body['change_train_details'] = request.change_train_details_shrink
        if not UtilClient.is_unset(request.distribute_order_id):
            body['distribute_order_id'] = request.distribute_order_id
        if not UtilClient.is_unset(request.order_id):
            body['order_id'] = request.order_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='TrainFeeCalculateChange',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/train/v1/change/fee',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.TrainFeeCalculateChangeResponse(),
            self.call_api(params, req, runtime)
        )

    async def train_fee_calculate_change_with_options_async(
        self,
        tmp_req: btrip_open_20220520_models.TrainFeeCalculateChangeRequest,
        headers: btrip_open_20220520_models.TrainFeeCalculateChangeHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.TrainFeeCalculateChangeResponse:
        """
        @summary 火车票改签费用预估
        
        @param tmp_req: TrainFeeCalculateChangeRequest
        @param headers: TrainFeeCalculateChangeHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: TrainFeeCalculateChangeResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.TrainFeeCalculateChangeShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.change_train_details):
            request.change_train_details_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.change_train_details, 'change_train_details', 'json')
        body = {}
        if not UtilClient.is_unset(request.change_train_details_shrink):
            body['change_train_details'] = request.change_train_details_shrink
        if not UtilClient.is_unset(request.distribute_order_id):
            body['distribute_order_id'] = request.distribute_order_id
        if not UtilClient.is_unset(request.order_id):
            body['order_id'] = request.order_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='TrainFeeCalculateChange',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/train/v1/change/fee',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.TrainFeeCalculateChangeResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def train_fee_calculate_change(
        self,
        request: btrip_open_20220520_models.TrainFeeCalculateChangeRequest,
    ) -> btrip_open_20220520_models.TrainFeeCalculateChangeResponse:
        """
        @summary 火车票改签费用预估
        
        @param request: TrainFeeCalculateChangeRequest
        @return: TrainFeeCalculateChangeResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.TrainFeeCalculateChangeHeaders()
        return self.train_fee_calculate_change_with_options(request, headers, runtime)

    async def train_fee_calculate_change_async(
        self,
        request: btrip_open_20220520_models.TrainFeeCalculateChangeRequest,
    ) -> btrip_open_20220520_models.TrainFeeCalculateChangeResponse:
        """
        @summary 火车票改签费用预估
        
        @param request: TrainFeeCalculateChangeRequest
        @return: TrainFeeCalculateChangeResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.TrainFeeCalculateChangeHeaders()
        return await self.train_fee_calculate_change_with_options_async(request, headers, runtime)

    def train_fee_calculate_refund_with_options(
        self,
        tmp_req: btrip_open_20220520_models.TrainFeeCalculateRefundRequest,
        headers: btrip_open_20220520_models.TrainFeeCalculateRefundHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.TrainFeeCalculateRefundResponse:
        """
        @summary 火车票退票费用预估
        
        @param tmp_req: TrainFeeCalculateRefundRequest
        @param headers: TrainFeeCalculateRefundHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: TrainFeeCalculateRefundResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.TrainFeeCalculateRefundShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.refund_train_infos):
            request.refund_train_infos_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.refund_train_infos, 'refund_train_infos', 'json')
        body = {}
        if not UtilClient.is_unset(request.distribute_order_id):
            body['distribute_order_id'] = request.distribute_order_id
        if not UtilClient.is_unset(request.order_id):
            body['order_id'] = request.order_id
        if not UtilClient.is_unset(request.refund_train_infos_shrink):
            body['refund_train_infos'] = request.refund_train_infos_shrink
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='TrainFeeCalculateRefund',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/train/v1/refund/fee',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.TrainFeeCalculateRefundResponse(),
            self.call_api(params, req, runtime)
        )

    async def train_fee_calculate_refund_with_options_async(
        self,
        tmp_req: btrip_open_20220520_models.TrainFeeCalculateRefundRequest,
        headers: btrip_open_20220520_models.TrainFeeCalculateRefundHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.TrainFeeCalculateRefundResponse:
        """
        @summary 火车票退票费用预估
        
        @param tmp_req: TrainFeeCalculateRefundRequest
        @param headers: TrainFeeCalculateRefundHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: TrainFeeCalculateRefundResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.TrainFeeCalculateRefundShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.refund_train_infos):
            request.refund_train_infos_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.refund_train_infos, 'refund_train_infos', 'json')
        body = {}
        if not UtilClient.is_unset(request.distribute_order_id):
            body['distribute_order_id'] = request.distribute_order_id
        if not UtilClient.is_unset(request.order_id):
            body['order_id'] = request.order_id
        if not UtilClient.is_unset(request.refund_train_infos_shrink):
            body['refund_train_infos'] = request.refund_train_infos_shrink
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='TrainFeeCalculateRefund',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/train/v1/refund/fee',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.TrainFeeCalculateRefundResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def train_fee_calculate_refund(
        self,
        request: btrip_open_20220520_models.TrainFeeCalculateRefundRequest,
    ) -> btrip_open_20220520_models.TrainFeeCalculateRefundResponse:
        """
        @summary 火车票退票费用预估
        
        @param request: TrainFeeCalculateRefundRequest
        @return: TrainFeeCalculateRefundResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.TrainFeeCalculateRefundHeaders()
        return self.train_fee_calculate_refund_with_options(request, headers, runtime)

    async def train_fee_calculate_refund_async(
        self,
        request: btrip_open_20220520_models.TrainFeeCalculateRefundRequest,
    ) -> btrip_open_20220520_models.TrainFeeCalculateRefundResponse:
        """
        @summary 火车票退票费用预估
        
        @param request: TrainFeeCalculateRefundRequest
        @return: TrainFeeCalculateRefundResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.TrainFeeCalculateRefundHeaders()
        return await self.train_fee_calculate_refund_with_options_async(request, headers, runtime)

    def train_no_info_search_with_options(
        self,
        request: btrip_open_20220520_models.TrainNoInfoSearchRequest,
        headers: btrip_open_20220520_models.TrainNoInfoSearchHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.TrainNoInfoSearchResponse:
        """
        @summary 火车票车次详情查询
        
        @param request: TrainNoInfoSearchRequest
        @param headers: TrainNoInfoSearchHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: TrainNoInfoSearchResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.arr_location):
            body['arr_location'] = request.arr_location
        if not UtilClient.is_unset(request.dep_date):
            body['dep_date'] = request.dep_date
        if not UtilClient.is_unset(request.dep_location):
            body['dep_location'] = request.dep_location
        if not UtilClient.is_unset(request.line_key):
            body['line_key'] = request.line_key
        if not UtilClient.is_unset(request.middle_date):
            body['middle_date'] = request.middle_date
        if not UtilClient.is_unset(request.middle_station):
            body['middle_station'] = request.middle_station
        if not UtilClient.is_unset(request.order_id):
            body['order_id'] = request.order_id
        if not UtilClient.is_unset(request.train_no):
            body['train_no'] = request.train_no
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='TrainNoInfoSearch',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/train/v1/search/info',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.TrainNoInfoSearchResponse(),
            self.call_api(params, req, runtime)
        )

    async def train_no_info_search_with_options_async(
        self,
        request: btrip_open_20220520_models.TrainNoInfoSearchRequest,
        headers: btrip_open_20220520_models.TrainNoInfoSearchHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.TrainNoInfoSearchResponse:
        """
        @summary 火车票车次详情查询
        
        @param request: TrainNoInfoSearchRequest
        @param headers: TrainNoInfoSearchHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: TrainNoInfoSearchResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.arr_location):
            body['arr_location'] = request.arr_location
        if not UtilClient.is_unset(request.dep_date):
            body['dep_date'] = request.dep_date
        if not UtilClient.is_unset(request.dep_location):
            body['dep_location'] = request.dep_location
        if not UtilClient.is_unset(request.line_key):
            body['line_key'] = request.line_key
        if not UtilClient.is_unset(request.middle_date):
            body['middle_date'] = request.middle_date
        if not UtilClient.is_unset(request.middle_station):
            body['middle_station'] = request.middle_station
        if not UtilClient.is_unset(request.order_id):
            body['order_id'] = request.order_id
        if not UtilClient.is_unset(request.train_no):
            body['train_no'] = request.train_no
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='TrainNoInfoSearch',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/train/v1/search/info',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.TrainNoInfoSearchResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def train_no_info_search(
        self,
        request: btrip_open_20220520_models.TrainNoInfoSearchRequest,
    ) -> btrip_open_20220520_models.TrainNoInfoSearchResponse:
        """
        @summary 火车票车次详情查询
        
        @param request: TrainNoInfoSearchRequest
        @return: TrainNoInfoSearchResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.TrainNoInfoSearchHeaders()
        return self.train_no_info_search_with_options(request, headers, runtime)

    async def train_no_info_search_async(
        self,
        request: btrip_open_20220520_models.TrainNoInfoSearchRequest,
    ) -> btrip_open_20220520_models.TrainNoInfoSearchResponse:
        """
        @summary 火车票车次详情查询
        
        @param request: TrainNoInfoSearchRequest
        @return: TrainNoInfoSearchResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.TrainNoInfoSearchHeaders()
        return await self.train_no_info_search_with_options_async(request, headers, runtime)

    def train_no_list_search_with_options(
        self,
        tmp_req: btrip_open_20220520_models.TrainNoListSearchRequest,
        headers: btrip_open_20220520_models.TrainNoListSearchHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.TrainNoListSearchResponse:
        """
        @summary 火车票车次列表查询
        
        @param tmp_req: TrainNoListSearchRequest
        @param headers: TrainNoListSearchHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: TrainNoListSearchResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.TrainNoListSearchShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.option):
            request.option_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.option, 'option', 'json')
        body = {}
        if not UtilClient.is_unset(request.arr_location):
            body['arr_location'] = request.arr_location
        if not UtilClient.is_unset(request.dep_date):
            body['dep_date'] = request.dep_date
        if not UtilClient.is_unset(request.dep_location):
            body['dep_location'] = request.dep_location
        if not UtilClient.is_unset(request.option_shrink):
            body['option'] = request.option_shrink
        if not UtilClient.is_unset(request.order_id):
            body['order_id'] = request.order_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='TrainNoListSearch',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/train/v1/search/list',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.TrainNoListSearchResponse(),
            self.call_api(params, req, runtime)
        )

    async def train_no_list_search_with_options_async(
        self,
        tmp_req: btrip_open_20220520_models.TrainNoListSearchRequest,
        headers: btrip_open_20220520_models.TrainNoListSearchHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.TrainNoListSearchResponse:
        """
        @summary 火车票车次列表查询
        
        @param tmp_req: TrainNoListSearchRequest
        @param headers: TrainNoListSearchHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: TrainNoListSearchResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.TrainNoListSearchShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.option):
            request.option_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.option, 'option', 'json')
        body = {}
        if not UtilClient.is_unset(request.arr_location):
            body['arr_location'] = request.arr_location
        if not UtilClient.is_unset(request.dep_date):
            body['dep_date'] = request.dep_date
        if not UtilClient.is_unset(request.dep_location):
            body['dep_location'] = request.dep_location
        if not UtilClient.is_unset(request.option_shrink):
            body['option'] = request.option_shrink
        if not UtilClient.is_unset(request.order_id):
            body['order_id'] = request.order_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='TrainNoListSearch',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/train/v1/search/list',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.TrainNoListSearchResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def train_no_list_search(
        self,
        request: btrip_open_20220520_models.TrainNoListSearchRequest,
    ) -> btrip_open_20220520_models.TrainNoListSearchResponse:
        """
        @summary 火车票车次列表查询
        
        @param request: TrainNoListSearchRequest
        @return: TrainNoListSearchResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.TrainNoListSearchHeaders()
        return self.train_no_list_search_with_options(request, headers, runtime)

    async def train_no_list_search_async(
        self,
        request: btrip_open_20220520_models.TrainNoListSearchRequest,
    ) -> btrip_open_20220520_models.TrainNoListSearchResponse:
        """
        @summary 火车票车次列表查询
        
        @param request: TrainNoListSearchRequest
        @return: TrainNoListSearchResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.TrainNoListSearchHeaders()
        return await self.train_no_list_search_with_options_async(request, headers, runtime)

    def train_order_cancel_with_options(
        self,
        request: btrip_open_20220520_models.TrainOrderCancelRequest,
        headers: btrip_open_20220520_models.TrainOrderCancelHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.TrainOrderCancelResponse:
        """
        @summary 火车票订单取消
        
        @param request: TrainOrderCancelRequest
        @param headers: TrainOrderCancelHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: TrainOrderCancelResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.change_order_id):
            body['change_order_id'] = request.change_order_id
        if not UtilClient.is_unset(request.order_id):
            body['order_id'] = request.order_id
        if not UtilClient.is_unset(request.out_change_order_id):
            body['out_change_order_id'] = request.out_change_order_id
        if not UtilClient.is_unset(request.out_order_id):
            body['out_order_id'] = request.out_order_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='TrainOrderCancel',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/train/v1/order/cancel',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.TrainOrderCancelResponse(),
            self.call_api(params, req, runtime)
        )

    async def train_order_cancel_with_options_async(
        self,
        request: btrip_open_20220520_models.TrainOrderCancelRequest,
        headers: btrip_open_20220520_models.TrainOrderCancelHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.TrainOrderCancelResponse:
        """
        @summary 火车票订单取消
        
        @param request: TrainOrderCancelRequest
        @param headers: TrainOrderCancelHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: TrainOrderCancelResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.change_order_id):
            body['change_order_id'] = request.change_order_id
        if not UtilClient.is_unset(request.order_id):
            body['order_id'] = request.order_id
        if not UtilClient.is_unset(request.out_change_order_id):
            body['out_change_order_id'] = request.out_change_order_id
        if not UtilClient.is_unset(request.out_order_id):
            body['out_order_id'] = request.out_order_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='TrainOrderCancel',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/train/v1/order/cancel',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.TrainOrderCancelResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def train_order_cancel(
        self,
        request: btrip_open_20220520_models.TrainOrderCancelRequest,
    ) -> btrip_open_20220520_models.TrainOrderCancelResponse:
        """
        @summary 火车票订单取消
        
        @param request: TrainOrderCancelRequest
        @return: TrainOrderCancelResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.TrainOrderCancelHeaders()
        return self.train_order_cancel_with_options(request, headers, runtime)

    async def train_order_cancel_async(
        self,
        request: btrip_open_20220520_models.TrainOrderCancelRequest,
    ) -> btrip_open_20220520_models.TrainOrderCancelResponse:
        """
        @summary 火车票订单取消
        
        @param request: TrainOrderCancelRequest
        @return: TrainOrderCancelResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.TrainOrderCancelHeaders()
        return await self.train_order_cancel_with_options_async(request, headers, runtime)

    def train_order_change_confirm_with_options(
        self,
        request: btrip_open_20220520_models.TrainOrderChangeConfirmRequest,
        headers: btrip_open_20220520_models.TrainOrderChangeConfirmHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.TrainOrderChangeConfirmResponse:
        """
        @summary 火车票改签确认
        
        @param request: TrainOrderChangeConfirmRequest
        @param headers: TrainOrderChangeConfirmHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: TrainOrderChangeConfirmResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.change_apply_id):
            body['change_apply_id'] = request.change_apply_id
        if not UtilClient.is_unset(request.change_settle_amount):
            body['change_settle_amount'] = request.change_settle_amount
        if not UtilClient.is_unset(request.order_id):
            body['order_id'] = request.order_id
        if not UtilClient.is_unset(request.out_change_apply_id):
            body['out_change_apply_id'] = request.out_change_apply_id
        if not UtilClient.is_unset(request.out_order_id):
            body['out_order_id'] = request.out_order_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='TrainOrderChangeConfirm',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/train/v1/change/confirm',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.TrainOrderChangeConfirmResponse(),
            self.call_api(params, req, runtime)
        )

    async def train_order_change_confirm_with_options_async(
        self,
        request: btrip_open_20220520_models.TrainOrderChangeConfirmRequest,
        headers: btrip_open_20220520_models.TrainOrderChangeConfirmHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.TrainOrderChangeConfirmResponse:
        """
        @summary 火车票改签确认
        
        @param request: TrainOrderChangeConfirmRequest
        @param headers: TrainOrderChangeConfirmHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: TrainOrderChangeConfirmResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.change_apply_id):
            body['change_apply_id'] = request.change_apply_id
        if not UtilClient.is_unset(request.change_settle_amount):
            body['change_settle_amount'] = request.change_settle_amount
        if not UtilClient.is_unset(request.order_id):
            body['order_id'] = request.order_id
        if not UtilClient.is_unset(request.out_change_apply_id):
            body['out_change_apply_id'] = request.out_change_apply_id
        if not UtilClient.is_unset(request.out_order_id):
            body['out_order_id'] = request.out_order_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='TrainOrderChangeConfirm',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/train/v1/change/confirm',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.TrainOrderChangeConfirmResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def train_order_change_confirm(
        self,
        request: btrip_open_20220520_models.TrainOrderChangeConfirmRequest,
    ) -> btrip_open_20220520_models.TrainOrderChangeConfirmResponse:
        """
        @summary 火车票改签确认
        
        @param request: TrainOrderChangeConfirmRequest
        @return: TrainOrderChangeConfirmResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.TrainOrderChangeConfirmHeaders()
        return self.train_order_change_confirm_with_options(request, headers, runtime)

    async def train_order_change_confirm_async(
        self,
        request: btrip_open_20220520_models.TrainOrderChangeConfirmRequest,
    ) -> btrip_open_20220520_models.TrainOrderChangeConfirmResponse:
        """
        @summary 火车票改签确认
        
        @param request: TrainOrderChangeConfirmRequest
        @return: TrainOrderChangeConfirmResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.TrainOrderChangeConfirmHeaders()
        return await self.train_order_change_confirm_with_options_async(request, headers, runtime)

    def train_order_create_with_options(
        self,
        tmp_req: btrip_open_20220520_models.TrainOrderCreateRequest,
        headers: btrip_open_20220520_models.TrainOrderCreateHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.TrainOrderCreateResponse:
        """
        @summary 火车票正向预订
        
        @param tmp_req: TrainOrderCreateRequest
        @param headers: TrainOrderCreateHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: TrainOrderCreateResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.TrainOrderCreateShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.book_train_infos):
            request.book_train_infos_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.book_train_infos, 'book_train_infos', 'json')
        if not UtilClient.is_unset(tmp_req.business_info):
            request.business_info_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.business_info, 'business_info', 'json')
        if not UtilClient.is_unset(tmp_req.contact_info):
            request.contact_info_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.contact_info, 'contact_info', 'json')
        if not UtilClient.is_unset(tmp_req.passenger_open_info_s):
            request.passenger_open_info_sshrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.passenger_open_info_s, 'passenger_open_info_s', 'json')
        body = {}
        if not UtilClient.is_unset(request.accept_no_seat):
            body['accept_no_seat'] = request.accept_no_seat
        if not UtilClient.is_unset(request.book_train_infos_shrink):
            body['book_train_infos'] = request.book_train_infos_shrink
        if not UtilClient.is_unset(request.btrip_user_id):
            body['btrip_user_id'] = request.btrip_user_id
        if not UtilClient.is_unset(request.btrip_user_name):
            body['btrip_user_name'] = request.btrip_user_name
        if not UtilClient.is_unset(request.business_info_shrink):
            body['business_info'] = request.business_info_shrink
        if not UtilClient.is_unset(request.contact_info_shrink):
            body['contact_info'] = request.contact_info_shrink
        if not UtilClient.is_unset(request.force_match):
            body['force_match'] = request.force_match
        if not UtilClient.is_unset(request.is_pay_now):
            body['is_pay_now'] = request.is_pay_now
        if not UtilClient.is_unset(request.out_order_id):
            body['out_order_id'] = request.out_order_id
        if not UtilClient.is_unset(request.passenger_open_info_sshrink):
            body['passenger_open_info_s'] = request.passenger_open_info_sshrink
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='TrainOrderCreate',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/train/v1/order/create',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.TrainOrderCreateResponse(),
            self.call_api(params, req, runtime)
        )

    async def train_order_create_with_options_async(
        self,
        tmp_req: btrip_open_20220520_models.TrainOrderCreateRequest,
        headers: btrip_open_20220520_models.TrainOrderCreateHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.TrainOrderCreateResponse:
        """
        @summary 火车票正向预订
        
        @param tmp_req: TrainOrderCreateRequest
        @param headers: TrainOrderCreateHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: TrainOrderCreateResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.TrainOrderCreateShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.book_train_infos):
            request.book_train_infos_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.book_train_infos, 'book_train_infos', 'json')
        if not UtilClient.is_unset(tmp_req.business_info):
            request.business_info_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.business_info, 'business_info', 'json')
        if not UtilClient.is_unset(tmp_req.contact_info):
            request.contact_info_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.contact_info, 'contact_info', 'json')
        if not UtilClient.is_unset(tmp_req.passenger_open_info_s):
            request.passenger_open_info_sshrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.passenger_open_info_s, 'passenger_open_info_s', 'json')
        body = {}
        if not UtilClient.is_unset(request.accept_no_seat):
            body['accept_no_seat'] = request.accept_no_seat
        if not UtilClient.is_unset(request.book_train_infos_shrink):
            body['book_train_infos'] = request.book_train_infos_shrink
        if not UtilClient.is_unset(request.btrip_user_id):
            body['btrip_user_id'] = request.btrip_user_id
        if not UtilClient.is_unset(request.btrip_user_name):
            body['btrip_user_name'] = request.btrip_user_name
        if not UtilClient.is_unset(request.business_info_shrink):
            body['business_info'] = request.business_info_shrink
        if not UtilClient.is_unset(request.contact_info_shrink):
            body['contact_info'] = request.contact_info_shrink
        if not UtilClient.is_unset(request.force_match):
            body['force_match'] = request.force_match
        if not UtilClient.is_unset(request.is_pay_now):
            body['is_pay_now'] = request.is_pay_now
        if not UtilClient.is_unset(request.out_order_id):
            body['out_order_id'] = request.out_order_id
        if not UtilClient.is_unset(request.passenger_open_info_sshrink):
            body['passenger_open_info_s'] = request.passenger_open_info_sshrink
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='TrainOrderCreate',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/train/v1/order/create',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.TrainOrderCreateResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def train_order_create(
        self,
        request: btrip_open_20220520_models.TrainOrderCreateRequest,
    ) -> btrip_open_20220520_models.TrainOrderCreateResponse:
        """
        @summary 火车票正向预订
        
        @param request: TrainOrderCreateRequest
        @return: TrainOrderCreateResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.TrainOrderCreateHeaders()
        return self.train_order_create_with_options(request, headers, runtime)

    async def train_order_create_async(
        self,
        request: btrip_open_20220520_models.TrainOrderCreateRequest,
    ) -> btrip_open_20220520_models.TrainOrderCreateResponse:
        """
        @summary 火车票正向预订
        
        @param request: TrainOrderCreateRequest
        @return: TrainOrderCreateResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.TrainOrderCreateHeaders()
        return await self.train_order_create_with_options_async(request, headers, runtime)

    def train_order_detail_query_with_options(
        self,
        request: btrip_open_20220520_models.TrainOrderDetailQueryRequest,
        headers: btrip_open_20220520_models.TrainOrderDetailQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.TrainOrderDetailQueryResponse:
        """
        @summary 火车票订单详情
        
        @param request: TrainOrderDetailQueryRequest
        @param headers: TrainOrderDetailQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: TrainOrderDetailQueryResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.order_id):
            body['order_id'] = request.order_id
        if not UtilClient.is_unset(request.out_order_id):
            body['out_order_id'] = request.out_order_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='TrainOrderDetailQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/train/v1/order/query',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.TrainOrderDetailQueryResponse(),
            self.call_api(params, req, runtime)
        )

    async def train_order_detail_query_with_options_async(
        self,
        request: btrip_open_20220520_models.TrainOrderDetailQueryRequest,
        headers: btrip_open_20220520_models.TrainOrderDetailQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.TrainOrderDetailQueryResponse:
        """
        @summary 火车票订单详情
        
        @param request: TrainOrderDetailQueryRequest
        @param headers: TrainOrderDetailQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: TrainOrderDetailQueryResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.order_id):
            body['order_id'] = request.order_id
        if not UtilClient.is_unset(request.out_order_id):
            body['out_order_id'] = request.out_order_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='TrainOrderDetailQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/train/v1/order/query',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.TrainOrderDetailQueryResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def train_order_detail_query(
        self,
        request: btrip_open_20220520_models.TrainOrderDetailQueryRequest,
    ) -> btrip_open_20220520_models.TrainOrderDetailQueryResponse:
        """
        @summary 火车票订单详情
        
        @param request: TrainOrderDetailQueryRequest
        @return: TrainOrderDetailQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.TrainOrderDetailQueryHeaders()
        return self.train_order_detail_query_with_options(request, headers, runtime)

    async def train_order_detail_query_async(
        self,
        request: btrip_open_20220520_models.TrainOrderDetailQueryRequest,
    ) -> btrip_open_20220520_models.TrainOrderDetailQueryResponse:
        """
        @summary 火车票订单详情
        
        @param request: TrainOrderDetailQueryRequest
        @return: TrainOrderDetailQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.TrainOrderDetailQueryHeaders()
        return await self.train_order_detail_query_with_options_async(request, headers, runtime)

    def train_order_list_query_with_options(
        self,
        request: btrip_open_20220520_models.TrainOrderListQueryRequest,
        headers: btrip_open_20220520_models.TrainOrderListQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.TrainOrderListQueryResponse:
        """
        @summary 查询火车票订单列表
        
        @param request: TrainOrderListQueryRequest
        @param headers: TrainOrderListQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: TrainOrderListQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.all_apply):
            query['all_apply'] = request.all_apply
        if not UtilClient.is_unset(request.apply_id):
            query['apply_id'] = request.apply_id
        if not UtilClient.is_unset(request.depart_id):
            query['depart_id'] = request.depart_id
        if not UtilClient.is_unset(request.end_time):
            query['end_time'] = request.end_time
        if not UtilClient.is_unset(request.page):
            query['page'] = request.page
        if not UtilClient.is_unset(request.page_size):
            query['page_size'] = request.page_size
        if not UtilClient.is_unset(request.start_time):
            query['start_time'] = request.start_time
        if not UtilClient.is_unset(request.thirdpart_apply_id):
            query['thirdpart_apply_id'] = request.thirdpart_apply_id
        if not UtilClient.is_unset(request.update_end_time):
            query['update_end_time'] = request.update_end_time
        if not UtilClient.is_unset(request.update_start_time):
            query['update_start_time'] = request.update_start_time
        if not UtilClient.is_unset(request.user_id):
            query['user_id'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='TrainOrderListQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/train/v1/order-list',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.TrainOrderListQueryResponse(),
            self.call_api(params, req, runtime)
        )

    async def train_order_list_query_with_options_async(
        self,
        request: btrip_open_20220520_models.TrainOrderListQueryRequest,
        headers: btrip_open_20220520_models.TrainOrderListQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.TrainOrderListQueryResponse:
        """
        @summary 查询火车票订单列表
        
        @param request: TrainOrderListQueryRequest
        @param headers: TrainOrderListQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: TrainOrderListQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.all_apply):
            query['all_apply'] = request.all_apply
        if not UtilClient.is_unset(request.apply_id):
            query['apply_id'] = request.apply_id
        if not UtilClient.is_unset(request.depart_id):
            query['depart_id'] = request.depart_id
        if not UtilClient.is_unset(request.end_time):
            query['end_time'] = request.end_time
        if not UtilClient.is_unset(request.page):
            query['page'] = request.page
        if not UtilClient.is_unset(request.page_size):
            query['page_size'] = request.page_size
        if not UtilClient.is_unset(request.start_time):
            query['start_time'] = request.start_time
        if not UtilClient.is_unset(request.thirdpart_apply_id):
            query['thirdpart_apply_id'] = request.thirdpart_apply_id
        if not UtilClient.is_unset(request.update_end_time):
            query['update_end_time'] = request.update_end_time
        if not UtilClient.is_unset(request.update_start_time):
            query['update_start_time'] = request.update_start_time
        if not UtilClient.is_unset(request.user_id):
            query['user_id'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='TrainOrderListQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/train/v1/order-list',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.TrainOrderListQueryResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def train_order_list_query(
        self,
        request: btrip_open_20220520_models.TrainOrderListQueryRequest,
    ) -> btrip_open_20220520_models.TrainOrderListQueryResponse:
        """
        @summary 查询火车票订单列表
        
        @param request: TrainOrderListQueryRequest
        @return: TrainOrderListQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.TrainOrderListQueryHeaders()
        return self.train_order_list_query_with_options(request, headers, runtime)

    async def train_order_list_query_async(
        self,
        request: btrip_open_20220520_models.TrainOrderListQueryRequest,
    ) -> btrip_open_20220520_models.TrainOrderListQueryResponse:
        """
        @summary 查询火车票订单列表
        
        @param request: TrainOrderListQueryRequest
        @return: TrainOrderListQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.TrainOrderListQueryHeaders()
        return await self.train_order_list_query_with_options_async(request, headers, runtime)

    def train_order_pay_with_options(
        self,
        request: btrip_open_20220520_models.TrainOrderPayRequest,
        headers: btrip_open_20220520_models.TrainOrderPayHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.TrainOrderPayResponse:
        """
        @summary 火车票订单支付
        
        @param request: TrainOrderPayRequest
        @param headers: TrainOrderPayHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: TrainOrderPayResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.order_id):
            body['order_id'] = request.order_id
        if not UtilClient.is_unset(request.out_order_id):
            body['out_order_id'] = request.out_order_id
        if not UtilClient.is_unset(request.pay_amount):
            body['pay_amount'] = request.pay_amount
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='TrainOrderPay',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/train/v1/order/pay',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.TrainOrderPayResponse(),
            self.call_api(params, req, runtime)
        )

    async def train_order_pay_with_options_async(
        self,
        request: btrip_open_20220520_models.TrainOrderPayRequest,
        headers: btrip_open_20220520_models.TrainOrderPayHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.TrainOrderPayResponse:
        """
        @summary 火车票订单支付
        
        @param request: TrainOrderPayRequest
        @param headers: TrainOrderPayHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: TrainOrderPayResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.order_id):
            body['order_id'] = request.order_id
        if not UtilClient.is_unset(request.out_order_id):
            body['out_order_id'] = request.out_order_id
        if not UtilClient.is_unset(request.pay_amount):
            body['pay_amount'] = request.pay_amount
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='TrainOrderPay',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/train/v1/order/pay',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.TrainOrderPayResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def train_order_pay(
        self,
        request: btrip_open_20220520_models.TrainOrderPayRequest,
    ) -> btrip_open_20220520_models.TrainOrderPayResponse:
        """
        @summary 火车票订单支付
        
        @param request: TrainOrderPayRequest
        @return: TrainOrderPayResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.TrainOrderPayHeaders()
        return self.train_order_pay_with_options(request, headers, runtime)

    async def train_order_pay_async(
        self,
        request: btrip_open_20220520_models.TrainOrderPayRequest,
    ) -> btrip_open_20220520_models.TrainOrderPayResponse:
        """
        @summary 火车票订单支付
        
        @param request: TrainOrderPayRequest
        @return: TrainOrderPayResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.TrainOrderPayHeaders()
        return await self.train_order_pay_with_options_async(request, headers, runtime)

    def train_order_query_with_options(
        self,
        request: btrip_open_20220520_models.TrainOrderQueryRequest,
        headers: btrip_open_20220520_models.TrainOrderQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.TrainOrderQueryResponse:
        """
        @summary 查询火车票订单详情（含票信息）
        
        @param request: TrainOrderQueryRequest
        @param headers: TrainOrderQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: TrainOrderQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.order_id):
            query['order_id'] = request.order_id
        if not UtilClient.is_unset(request.user_id):
            query['user_id'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='TrainOrderQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/train/v1/order',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.TrainOrderQueryResponse(),
            self.call_api(params, req, runtime)
        )

    async def train_order_query_with_options_async(
        self,
        request: btrip_open_20220520_models.TrainOrderQueryRequest,
        headers: btrip_open_20220520_models.TrainOrderQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.TrainOrderQueryResponse:
        """
        @summary 查询火车票订单详情（含票信息）
        
        @param request: TrainOrderQueryRequest
        @param headers: TrainOrderQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: TrainOrderQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.order_id):
            query['order_id'] = request.order_id
        if not UtilClient.is_unset(request.user_id):
            query['user_id'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='TrainOrderQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/train/v1/order',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.TrainOrderQueryResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def train_order_query(
        self,
        request: btrip_open_20220520_models.TrainOrderQueryRequest,
    ) -> btrip_open_20220520_models.TrainOrderQueryResponse:
        """
        @summary 查询火车票订单详情（含票信息）
        
        @param request: TrainOrderQueryRequest
        @return: TrainOrderQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.TrainOrderQueryHeaders()
        return self.train_order_query_with_options(request, headers, runtime)

    async def train_order_query_async(
        self,
        request: btrip_open_20220520_models.TrainOrderQueryRequest,
    ) -> btrip_open_20220520_models.TrainOrderQueryResponse:
        """
        @summary 查询火车票订单详情（含票信息）
        
        @param request: TrainOrderQueryRequest
        @return: TrainOrderQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.TrainOrderQueryHeaders()
        return await self.train_order_query_with_options_async(request, headers, runtime)

    def train_order_query_v2with_options(
        self,
        request: btrip_open_20220520_models.TrainOrderQueryV2Request,
        headers: btrip_open_20220520_models.TrainOrderQueryV2Headers,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.TrainOrderQueryV2Response:
        """
        @summary 火车票订单查询V2
        
        @param request: TrainOrderQueryV2Request
        @param headers: TrainOrderQueryV2Headers
        @param runtime: runtime options for this request RuntimeOptions
        @return: TrainOrderQueryV2Response
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.order_id):
            query['order_id'] = request.order_id
        if not UtilClient.is_unset(request.user_id):
            query['user_id'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='TrainOrderQueryV2',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/train/v2/order',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.TrainOrderQueryV2Response(),
            self.call_api(params, req, runtime)
        )

    async def train_order_query_v2with_options_async(
        self,
        request: btrip_open_20220520_models.TrainOrderQueryV2Request,
        headers: btrip_open_20220520_models.TrainOrderQueryV2Headers,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.TrainOrderQueryV2Response:
        """
        @summary 火车票订单查询V2
        
        @param request: TrainOrderQueryV2Request
        @param headers: TrainOrderQueryV2Headers
        @param runtime: runtime options for this request RuntimeOptions
        @return: TrainOrderQueryV2Response
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.order_id):
            query['order_id'] = request.order_id
        if not UtilClient.is_unset(request.user_id):
            query['user_id'] = request.user_id
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='TrainOrderQueryV2',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/train/v2/order',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.TrainOrderQueryV2Response(),
            await self.call_api_async(params, req, runtime)
        )

    def train_order_query_v2(
        self,
        request: btrip_open_20220520_models.TrainOrderQueryV2Request,
    ) -> btrip_open_20220520_models.TrainOrderQueryV2Response:
        """
        @summary 火车票订单查询V2
        
        @param request: TrainOrderQueryV2Request
        @return: TrainOrderQueryV2Response
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.TrainOrderQueryV2Headers()
        return self.train_order_query_v2with_options(request, headers, runtime)

    async def train_order_query_v2_async(
        self,
        request: btrip_open_20220520_models.TrainOrderQueryV2Request,
    ) -> btrip_open_20220520_models.TrainOrderQueryV2Response:
        """
        @summary 火车票订单查询V2
        
        @param request: TrainOrderQueryV2Request
        @return: TrainOrderQueryV2Response
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.TrainOrderQueryV2Headers()
        return await self.train_order_query_v2with_options_async(request, headers, runtime)

    def train_station_search_with_options(
        self,
        request: btrip_open_20220520_models.TrainStationSearchRequest,
        headers: btrip_open_20220520_models.TrainStationSearchHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.TrainStationSearchResponse:
        """
        @summary 查询火车站数据
        
        @param request: TrainStationSearchRequest
        @param headers: TrainStationSearchHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: TrainStationSearchResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.keyword):
            query['keyword'] = request.keyword
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='TrainStationSearch',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/city/v1/train',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.TrainStationSearchResponse(),
            self.call_api(params, req, runtime)
        )

    async def train_station_search_with_options_async(
        self,
        request: btrip_open_20220520_models.TrainStationSearchRequest,
        headers: btrip_open_20220520_models.TrainStationSearchHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.TrainStationSearchResponse:
        """
        @summary 查询火车站数据
        
        @param request: TrainStationSearchRequest
        @param headers: TrainStationSearchHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: TrainStationSearchResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.keyword):
            query['keyword'] = request.keyword
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='TrainStationSearch',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/city/v1/train',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.TrainStationSearchResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def train_station_search(
        self,
        request: btrip_open_20220520_models.TrainStationSearchRequest,
    ) -> btrip_open_20220520_models.TrainStationSearchResponse:
        """
        @summary 查询火车站数据
        
        @param request: TrainStationSearchRequest
        @return: TrainStationSearchResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.TrainStationSearchHeaders()
        return self.train_station_search_with_options(request, headers, runtime)

    async def train_station_search_async(
        self,
        request: btrip_open_20220520_models.TrainStationSearchRequest,
    ) -> btrip_open_20220520_models.TrainStationSearchResponse:
        """
        @summary 查询火车站数据
        
        @param request: TrainStationSearchRequest
        @return: TrainStationSearchResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.TrainStationSearchHeaders()
        return await self.train_station_search_with_options_async(request, headers, runtime)

    def train_stopover_search_with_options(
        self,
        request: btrip_open_20220520_models.TrainStopoverSearchRequest,
        headers: btrip_open_20220520_models.TrainStopoverSearchHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.TrainStopoverSearchResponse:
        """
        @summary 火车票经停站查询
        
        @param request: TrainStopoverSearchRequest
        @param headers: TrainStopoverSearchHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: TrainStopoverSearchResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.arr_station):
            body['arr_station'] = request.arr_station
        if not UtilClient.is_unset(request.dep_station):
            body['dep_station'] = request.dep_station
        if not UtilClient.is_unset(request.train_date):
            body['train_date'] = request.train_date
        if not UtilClient.is_unset(request.train_no):
            body['train_no'] = request.train_no
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='TrainStopoverSearch',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/train/v1/search/stopover',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.TrainStopoverSearchResponse(),
            self.call_api(params, req, runtime)
        )

    async def train_stopover_search_with_options_async(
        self,
        request: btrip_open_20220520_models.TrainStopoverSearchRequest,
        headers: btrip_open_20220520_models.TrainStopoverSearchHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.TrainStopoverSearchResponse:
        """
        @summary 火车票经停站查询
        
        @param request: TrainStopoverSearchRequest
        @param headers: TrainStopoverSearchHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: TrainStopoverSearchResponse
        """
        UtilClient.validate_model(request)
        body = {}
        if not UtilClient.is_unset(request.arr_station):
            body['arr_station'] = request.arr_station
        if not UtilClient.is_unset(request.dep_station):
            body['dep_station'] = request.dep_station
        if not UtilClient.is_unset(request.train_date):
            body['train_date'] = request.train_date
        if not UtilClient.is_unset(request.train_no):
            body['train_no'] = request.train_no
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            body=OpenApiUtilClient.parse_to_map(body)
        )
        params = open_api_models.Params(
            action='TrainStopoverSearch',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/train/v1/search/stopover',
            method='POST',
            auth_type='AK',
            style='ROA',
            req_body_type='formData',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.TrainStopoverSearchResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def train_stopover_search(
        self,
        request: btrip_open_20220520_models.TrainStopoverSearchRequest,
    ) -> btrip_open_20220520_models.TrainStopoverSearchResponse:
        """
        @summary 火车票经停站查询
        
        @param request: TrainStopoverSearchRequest
        @return: TrainStopoverSearchResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.TrainStopoverSearchHeaders()
        return self.train_stopover_search_with_options(request, headers, runtime)

    async def train_stopover_search_async(
        self,
        request: btrip_open_20220520_models.TrainStopoverSearchRequest,
    ) -> btrip_open_20220520_models.TrainStopoverSearchResponse:
        """
        @summary 火车票经停站查询
        
        @param request: TrainStopoverSearchRequest
        @return: TrainStopoverSearchResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.TrainStopoverSearchHeaders()
        return await self.train_stopover_search_with_options_async(request, headers, runtime)

    def train_ticket_scan_query_with_options(
        self,
        request: btrip_open_20220520_models.TrainTicketScanQueryRequest,
        headers: btrip_open_20220520_models.TrainTicketScanQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.TrainTicketScanQueryResponse:
        """
        @summary 查询火车票凭证扫描件
        
        @param request: TrainTicketScanQueryRequest
        @param headers: TrainTicketScanQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: TrainTicketScanQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.bill_date):
            query['bill_date'] = request.bill_date
        if not UtilClient.is_unset(request.bill_id):
            query['bill_id'] = request.bill_id
        if not UtilClient.is_unset(request.invoice_sub_task_id):
            query['invoice_sub_task_id'] = request.invoice_sub_task_id
        if not UtilClient.is_unset(request.page_no):
            query['page_no'] = request.page_no
        if not UtilClient.is_unset(request.page_size):
            query['page_size'] = request.page_size
        if not UtilClient.is_unset(request.serial_number):
            query['serial_number'] = request.serial_number
        if not UtilClient.is_unset(request.ticket_no):
            query['ticket_no'] = request.ticket_no
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='TrainTicketScanQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/scan/v1/train-ticket',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.TrainTicketScanQueryResponse(),
            self.call_api(params, req, runtime)
        )

    async def train_ticket_scan_query_with_options_async(
        self,
        request: btrip_open_20220520_models.TrainTicketScanQueryRequest,
        headers: btrip_open_20220520_models.TrainTicketScanQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.TrainTicketScanQueryResponse:
        """
        @summary 查询火车票凭证扫描件
        
        @param request: TrainTicketScanQueryRequest
        @param headers: TrainTicketScanQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: TrainTicketScanQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.bill_date):
            query['bill_date'] = request.bill_date
        if not UtilClient.is_unset(request.bill_id):
            query['bill_id'] = request.bill_id
        if not UtilClient.is_unset(request.invoice_sub_task_id):
            query['invoice_sub_task_id'] = request.invoice_sub_task_id
        if not UtilClient.is_unset(request.page_no):
            query['page_no'] = request.page_no
        if not UtilClient.is_unset(request.page_size):
            query['page_size'] = request.page_size
        if not UtilClient.is_unset(request.serial_number):
            query['serial_number'] = request.serial_number
        if not UtilClient.is_unset(request.ticket_no):
            query['ticket_no'] = request.ticket_no
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='TrainTicketScanQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/scan/v1/train-ticket',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.TrainTicketScanQueryResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def train_ticket_scan_query(
        self,
        request: btrip_open_20220520_models.TrainTicketScanQueryRequest,
    ) -> btrip_open_20220520_models.TrainTicketScanQueryResponse:
        """
        @summary 查询火车票凭证扫描件
        
        @param request: TrainTicketScanQueryRequest
        @return: TrainTicketScanQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.TrainTicketScanQueryHeaders()
        return self.train_ticket_scan_query_with_options(request, headers, runtime)

    async def train_ticket_scan_query_async(
        self,
        request: btrip_open_20220520_models.TrainTicketScanQueryRequest,
    ) -> btrip_open_20220520_models.TrainTicketScanQueryResponse:
        """
        @summary 查询火车票凭证扫描件
        
        @param request: TrainTicketScanQueryRequest
        @return: TrainTicketScanQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.TrainTicketScanQueryHeaders()
        return await self.train_ticket_scan_query_with_options_async(request, headers, runtime)

    def travel_standard_list_query_with_options(
        self,
        request: btrip_open_20220520_models.TravelStandardListQueryRequest,
        headers: btrip_open_20220520_models.TravelStandardListQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.TravelStandardListQueryResponse:
        """
        @summary 查询差标列表
        
        @param request: TravelStandardListQueryRequest
        @param headers: TravelStandardListQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: TravelStandardListQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.from_group):
            query['from_group'] = request.from_group
        if not UtilClient.is_unset(request.page_no):
            query['page_no'] = request.page_no
        if not UtilClient.is_unset(request.page_size):
            query['page_size'] = request.page_size
        if not UtilClient.is_unset(request.rule_name):
            query['rule_name'] = request.rule_name
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='TravelStandardListQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/travel-manage/v1/standards/list',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.TravelStandardListQueryResponse(),
            self.call_api(params, req, runtime)
        )

    async def travel_standard_list_query_with_options_async(
        self,
        request: btrip_open_20220520_models.TravelStandardListQueryRequest,
        headers: btrip_open_20220520_models.TravelStandardListQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.TravelStandardListQueryResponse:
        """
        @summary 查询差标列表
        
        @param request: TravelStandardListQueryRequest
        @param headers: TravelStandardListQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: TravelStandardListQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.from_group):
            query['from_group'] = request.from_group
        if not UtilClient.is_unset(request.page_no):
            query['page_no'] = request.page_no
        if not UtilClient.is_unset(request.page_size):
            query['page_size'] = request.page_size
        if not UtilClient.is_unset(request.rule_name):
            query['rule_name'] = request.rule_name
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='TravelStandardListQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/travel-manage/v1/standards/list',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.TravelStandardListQueryResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def travel_standard_list_query(
        self,
        request: btrip_open_20220520_models.TravelStandardListQueryRequest,
    ) -> btrip_open_20220520_models.TravelStandardListQueryResponse:
        """
        @summary 查询差标列表
        
        @param request: TravelStandardListQueryRequest
        @return: TravelStandardListQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.TravelStandardListQueryHeaders()
        return self.travel_standard_list_query_with_options(request, headers, runtime)

    async def travel_standard_list_query_async(
        self,
        request: btrip_open_20220520_models.TravelStandardListQueryRequest,
    ) -> btrip_open_20220520_models.TravelStandardListQueryResponse:
        """
        @summary 查询差标列表
        
        @param request: TravelStandardListQueryRequest
        @return: TravelStandardListQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.TravelStandardListQueryHeaders()
        return await self.travel_standard_list_query_with_options_async(request, headers, runtime)

    def travel_standard_query_with_options(
        self,
        tmp_req: btrip_open_20220520_models.TravelStandardQueryRequest,
        headers: btrip_open_20220520_models.TravelStandardQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.TravelStandardQueryResponse:
        """
        @summary 查询差标详情
        
        @param tmp_req: TravelStandardQueryRequest
        @param headers: TravelStandardQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: TravelStandardQueryResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.TravelStandardQueryShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.service_type_list):
            request.service_type_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.service_type_list, 'service_type_list', 'json')
        query = {}
        if not UtilClient.is_unset(request.from_group):
            query['from_group'] = request.from_group
        if not UtilClient.is_unset(request.rule_code):
            query['rule_code'] = request.rule_code
        if not UtilClient.is_unset(request.service_type_list_shrink):
            query['service_type_list'] = request.service_type_list_shrink
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='TravelStandardQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/travel-manage/v1/standards/detail',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.TravelStandardQueryResponse(),
            self.call_api(params, req, runtime)
        )

    async def travel_standard_query_with_options_async(
        self,
        tmp_req: btrip_open_20220520_models.TravelStandardQueryRequest,
        headers: btrip_open_20220520_models.TravelStandardQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.TravelStandardQueryResponse:
        """
        @summary 查询差标详情
        
        @param tmp_req: TravelStandardQueryRequest
        @param headers: TravelStandardQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: TravelStandardQueryResponse
        """
        UtilClient.validate_model(tmp_req)
        request = btrip_open_20220520_models.TravelStandardQueryShrinkRequest()
        OpenApiUtilClient.convert(tmp_req, request)
        if not UtilClient.is_unset(tmp_req.service_type_list):
            request.service_type_list_shrink = OpenApiUtilClient.array_to_string_with_specified_style(tmp_req.service_type_list, 'service_type_list', 'json')
        query = {}
        if not UtilClient.is_unset(request.from_group):
            query['from_group'] = request.from_group
        if not UtilClient.is_unset(request.rule_code):
            query['rule_code'] = request.rule_code
        if not UtilClient.is_unset(request.service_type_list_shrink):
            query['service_type_list'] = request.service_type_list_shrink
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_corp_token):
            real_headers['x-acs-btrip-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='TravelStandardQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/travel-manage/v1/standards/detail',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.TravelStandardQueryResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def travel_standard_query(
        self,
        request: btrip_open_20220520_models.TravelStandardQueryRequest,
    ) -> btrip_open_20220520_models.TravelStandardQueryResponse:
        """
        @summary 查询差标详情
        
        @param request: TravelStandardQueryRequest
        @return: TravelStandardQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.TravelStandardQueryHeaders()
        return self.travel_standard_query_with_options(request, headers, runtime)

    async def travel_standard_query_async(
        self,
        request: btrip_open_20220520_models.TravelStandardQueryRequest,
    ) -> btrip_open_20220520_models.TravelStandardQueryResponse:
        """
        @summary 查询差标详情
        
        @param request: TravelStandardQueryRequest
        @return: TravelStandardQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.TravelStandardQueryHeaders()
        return await self.travel_standard_query_with_options_async(request, headers, runtime)

    def user_query_with_options(
        self,
        request: btrip_open_20220520_models.UserQueryRequest,
        headers: btrip_open_20220520_models.UserQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.UserQueryResponse:
        """
        @summary 人员查询
        
        @param request: UserQueryRequest
        @param headers: UserQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: UserQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.modified_time_greater_or_equal_than):
            query['modified_time_greater_or_equal_than'] = request.modified_time_greater_or_equal_than
        if not UtilClient.is_unset(request.page_size):
            query['page_size'] = request.page_size
        if not UtilClient.is_unset(request.page_token):
            query['page_token'] = request.page_token
        if not UtilClient.is_unset(request.third_part_job_no):
            query['third_part_job_no'] = request.third_part_job_no
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='UserQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/user/v1/user',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.UserQueryResponse(),
            self.call_api(params, req, runtime)
        )

    async def user_query_with_options_async(
        self,
        request: btrip_open_20220520_models.UserQueryRequest,
        headers: btrip_open_20220520_models.UserQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.UserQueryResponse:
        """
        @summary 人员查询
        
        @param request: UserQueryRequest
        @param headers: UserQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: UserQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.modified_time_greater_or_equal_than):
            query['modified_time_greater_or_equal_than'] = request.modified_time_greater_or_equal_than
        if not UtilClient.is_unset(request.page_size):
            query['page_size'] = request.page_size
        if not UtilClient.is_unset(request.page_token):
            query['page_token'] = request.page_token
        if not UtilClient.is_unset(request.third_part_job_no):
            query['third_part_job_no'] = request.third_part_job_no
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='UserQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/user/v1/user',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.UserQueryResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def user_query(
        self,
        request: btrip_open_20220520_models.UserQueryRequest,
    ) -> btrip_open_20220520_models.UserQueryResponse:
        """
        @summary 人员查询
        
        @param request: UserQueryRequest
        @return: UserQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.UserQueryHeaders()
        return self.user_query_with_options(request, headers, runtime)

    async def user_query_async(
        self,
        request: btrip_open_20220520_models.UserQueryRequest,
    ) -> btrip_open_20220520_models.UserQueryResponse:
        """
        @summary 人员查询
        
        @param request: UserQueryRequest
        @return: UserQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.UserQueryHeaders()
        return await self.user_query_with_options_async(request, headers, runtime)

    def vat_invoice_scan_query_with_options(
        self,
        request: btrip_open_20220520_models.VatInvoiceScanQueryRequest,
        headers: btrip_open_20220520_models.VatInvoiceScanQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.VatInvoiceScanQueryResponse:
        """
        @summary 查询增值税发票扫描件
        
        @param request: VatInvoiceScanQueryRequest
        @param headers: VatInvoiceScanQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: VatInvoiceScanQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.bill_date):
            query['bill_date'] = request.bill_date
        if not UtilClient.is_unset(request.bill_id):
            query['bill_id'] = request.bill_id
        if not UtilClient.is_unset(request.invoice_sub_task_id):
            query['invoice_sub_task_id'] = request.invoice_sub_task_id
        if not UtilClient.is_unset(request.page_no):
            query['page_no'] = request.page_no
        if not UtilClient.is_unset(request.page_size):
            query['page_size'] = request.page_size
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='VatInvoiceScanQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/scan/v1/vat-invoice',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.VatInvoiceScanQueryResponse(),
            self.call_api(params, req, runtime)
        )

    async def vat_invoice_scan_query_with_options_async(
        self,
        request: btrip_open_20220520_models.VatInvoiceScanQueryRequest,
        headers: btrip_open_20220520_models.VatInvoiceScanQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.VatInvoiceScanQueryResponse:
        """
        @summary 查询增值税发票扫描件
        
        @param request: VatInvoiceScanQueryRequest
        @param headers: VatInvoiceScanQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: VatInvoiceScanQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.bill_date):
            query['bill_date'] = request.bill_date
        if not UtilClient.is_unset(request.bill_id):
            query['bill_id'] = request.bill_id
        if not UtilClient.is_unset(request.invoice_sub_task_id):
            query['invoice_sub_task_id'] = request.invoice_sub_task_id
        if not UtilClient.is_unset(request.page_no):
            query['page_no'] = request.page_no
        if not UtilClient.is_unset(request.page_size):
            query['page_size'] = request.page_size
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='VatInvoiceScanQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/scan/v1/vat-invoice',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.VatInvoiceScanQueryResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def vat_invoice_scan_query(
        self,
        request: btrip_open_20220520_models.VatInvoiceScanQueryRequest,
    ) -> btrip_open_20220520_models.VatInvoiceScanQueryResponse:
        """
        @summary 查询增值税发票扫描件
        
        @param request: VatInvoiceScanQueryRequest
        @return: VatInvoiceScanQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.VatInvoiceScanQueryHeaders()
        return self.vat_invoice_scan_query_with_options(request, headers, runtime)

    async def vat_invoice_scan_query_async(
        self,
        request: btrip_open_20220520_models.VatInvoiceScanQueryRequest,
    ) -> btrip_open_20220520_models.VatInvoiceScanQueryResponse:
        """
        @summary 查询增值税发票扫描件
        
        @param request: VatInvoiceScanQueryRequest
        @return: VatInvoiceScanQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.VatInvoiceScanQueryHeaders()
        return await self.vat_invoice_scan_query_with_options_async(request, headers, runtime)

    def wait_apply_invoice_task_detail_query_with_options(
        self,
        request: btrip_open_20220520_models.WaitApplyInvoiceTaskDetailQueryRequest,
        headers: btrip_open_20220520_models.WaitApplyInvoiceTaskDetailQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.WaitApplyInvoiceTaskDetailQueryResponse:
        """
        @summary 查询账期待申请的发票数据
        
        @param request: WaitApplyInvoiceTaskDetailQueryRequest
        @param headers: WaitApplyInvoiceTaskDetailQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: WaitApplyInvoiceTaskDetailQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.bill_date):
            query['bill_date'] = request.bill_date
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='WaitApplyInvoiceTaskDetailQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/invoice/v1/wait-apply-task',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.WaitApplyInvoiceTaskDetailQueryResponse(),
            self.call_api(params, req, runtime)
        )

    async def wait_apply_invoice_task_detail_query_with_options_async(
        self,
        request: btrip_open_20220520_models.WaitApplyInvoiceTaskDetailQueryRequest,
        headers: btrip_open_20220520_models.WaitApplyInvoiceTaskDetailQueryHeaders,
        runtime: util_models.RuntimeOptions,
    ) -> btrip_open_20220520_models.WaitApplyInvoiceTaskDetailQueryResponse:
        """
        @summary 查询账期待申请的发票数据
        
        @param request: WaitApplyInvoiceTaskDetailQueryRequest
        @param headers: WaitApplyInvoiceTaskDetailQueryHeaders
        @param runtime: runtime options for this request RuntimeOptions
        @return: WaitApplyInvoiceTaskDetailQueryResponse
        """
        UtilClient.validate_model(request)
        query = {}
        if not UtilClient.is_unset(request.bill_date):
            query['bill_date'] = request.bill_date
        real_headers = {}
        if not UtilClient.is_unset(headers.common_headers):
            real_headers = headers.common_headers
        if not UtilClient.is_unset(headers.x_acs_btrip_so_corp_token):
            real_headers['x-acs-btrip-so-corp-token'] = UtilClient.to_jsonstring(headers.x_acs_btrip_so_corp_token)
        req = open_api_models.OpenApiRequest(
            headers=real_headers,
            query=OpenApiUtilClient.query(query)
        )
        params = open_api_models.Params(
            action='WaitApplyInvoiceTaskDetailQuery',
            version='2022-05-20',
            protocol='HTTPS',
            pathname=f'/invoice/v1/wait-apply-task',
            method='GET',
            auth_type='AK',
            style='ROA',
            req_body_type='json',
            body_type='json'
        )
        return TeaCore.from_map(
            btrip_open_20220520_models.WaitApplyInvoiceTaskDetailQueryResponse(),
            await self.call_api_async(params, req, runtime)
        )

    def wait_apply_invoice_task_detail_query(
        self,
        request: btrip_open_20220520_models.WaitApplyInvoiceTaskDetailQueryRequest,
    ) -> btrip_open_20220520_models.WaitApplyInvoiceTaskDetailQueryResponse:
        """
        @summary 查询账期待申请的发票数据
        
        @param request: WaitApplyInvoiceTaskDetailQueryRequest
        @return: WaitApplyInvoiceTaskDetailQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.WaitApplyInvoiceTaskDetailQueryHeaders()
        return self.wait_apply_invoice_task_detail_query_with_options(request, headers, runtime)

    async def wait_apply_invoice_task_detail_query_async(
        self,
        request: btrip_open_20220520_models.WaitApplyInvoiceTaskDetailQueryRequest,
    ) -> btrip_open_20220520_models.WaitApplyInvoiceTaskDetailQueryResponse:
        """
        @summary 查询账期待申请的发票数据
        
        @param request: WaitApplyInvoiceTaskDetailQueryRequest
        @return: WaitApplyInvoiceTaskDetailQueryResponse
        """
        runtime = util_models.RuntimeOptions()
        headers = btrip_open_20220520_models.WaitApplyInvoiceTaskDetailQueryHeaders()
        return await self.wait_apply_invoice_task_detail_query_with_options_async(request, headers, runtime)
