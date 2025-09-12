"""Shopify GraphQL client for API interactions."""

import httpx
from typing import Dict, Any, List, Optional
from datetime import datetime

from ..config.settings import get_settings
from ..db.models import Shop

settings = get_settings()


class ShopifyClient:
    """Shopify GraphQL API client."""
    
    def __init__(self):
        self.api_version = settings.shopify_api_version
        self.base_url = None
    
    def _get_headers(self, access_token: str) -> Dict[str, str]:
        """Get headers for Shopify API requests."""
        return {
            'X-Shopify-Access-Token': access_token,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
    
    def _get_shop_url(self, shop: Shop) -> str:
        """Get shop-specific API URL."""
        return f"https://{shop.shop_domain}/admin/api/{self.api_version}"
    
    async def get_inventory_item_cost(
        self, 
        shop: Shop, 
        inventory_item_id: str
    ) -> Optional[float]:
        """Get unit cost for inventory item from Shopify."""
        query = """
        query getInventoryItem($id: ID!) {
            inventoryItem(id: $id) {
                id
                unitCost
                tracked
            }
        }
        """
        
        variables = {"id": f"gid://shopify/InventoryItem/{inventory_item_id}"}
        
        url = f"{self._get_shop_url(shop)}/graphql.json"
        headers = self._get_headers(shop.access_token)
        
        payload = {
            "query": query,
            "variables": variables
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=payload, headers=headers)
                response.raise_for_status()
                
                data = response.json()
                if 'errors' in data:
                    return None
                
                inventory_item = data.get('data', {}).get('inventoryItem')
                if inventory_item and inventory_item.get('tracked'):
                    return float(inventory_item.get('unitCost', 0))
                
                return None
            except Exception:
                return None
    
    async def get_order_details(
        self, 
        shop: Shop, 
        order_id: str
    ) -> Optional[Dict[str, Any]]:
        """Get detailed order information from Shopify."""
        query = """
        query getOrder($id: ID!) {
            order(id: $id) {
                id
                name
                createdAt
                updatedAt
                processedAt
                totalPriceSet {
                    shopMoney {
                        amount
                        currencyCode
                    }
                    presentmentMoney {
                        amount
                        currencyCode
                    }
                }
                totalDiscountsSet {
                    shopMoney {
                        amount
                        currencyCode
                    }
                    presentmentMoney {
                        amount
                        currencyCode
                    }
                }
                totalTaxSet {
                    shopMoney {
                        amount
                        currencyCode
                    }
                    presentmentMoney {
                        amount
                        currencyCode
                    }
                }
                totalShippingPriceSet {
                    shopMoney {
                        amount
                        currencyCode
                    }
                    presentmentMoney {
                        amount
                        currencyCode
                    }
                }
                financialStatus
                fulfillmentStatus
                customer {
                    id
                }
                lineItems(first: 250) {
                    edges {
                        node {
                            id
                            product {
                                id
                            }
                            variant {
                                id
                                inventoryItem {
                                    id
                                    unitCost
                                    tracked
                                }
                            }
                            quantity
                            originalUnitPriceSet {
                                shopMoney {
                                    amount
                                    currencyCode
                                }
                                presentmentMoney {
                                    amount
                                    currencyCode
                                }
                            }
                            discountedUnitPriceSet {
                                shopMoney {
                                    amount
                                    currencyCode
                                }
                                presentmentMoney {
                                    amount
                                    currencyCode
                                }
                            }
                            discountAllocations {
                                amount {
                                    amount
                                    currencyCode
                                }
                                discountApplication {
                                    ... on DiscountCodeApplication {
                                        code
                                    }
                                    ... on ScriptDiscountApplication {
                                        title
                                    }
                                    ... on AutomaticDiscountApplication {
                                        title
                                    }
                                }
                            }
                        }
                    }
                }
                refunds(first: 250) {
                    edges {
                        node {
                            id
                            createdAt
                            refundLineItems(first: 250) {
                                edges {
                                    node {
                                        id
                                        lineItem {
                                            id
                                        }
                                        quantity
                                        restockType
                                        subtotalSet {
                                            shopMoney {
                                                amount
                                                currencyCode
                                            }
                                            presentmentMoney {
                                                amount
                                                currencyCode
                                            }
                                        }
                                        totalTaxSet {
                                            shopMoney {
                                                amount
                                                currencyCode
                                            }
                                            presentmentMoney {
                                                amount
                                                currencyCode
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
                transactions(first: 250) {
                    edges {
                        node {
                            id
                            kind
                            status
                            gateway
                            amount {
                                amount
                                currencyCode
                            }
                            processedAt
                            fees {
                                amount {
                                    amount
                                    currencyCode
                                }
                                flatFee {
                                    amount
                                    currencyCode
                                }
                                rate
                                type
                            }
                        }
                    }
                }
            }
        }
        """
        
        variables = {"id": f"gid://shopify/Order/{order_id}"}
        
        url = f"{self._get_shop_url(shop)}/graphql.json"
        headers = self._get_headers(shop.access_token)
        
        payload = {
            "query": query,
            "variables": variables
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=payload, headers=headers)
                response.raise_for_status()
                
                data = response.json()
                if 'errors' in data:
                    return None
                
                return data.get('data', {}).get('order')
            except Exception:
                return None
    
    async def create_bulk_operation(
        self, 
        shop: Shop, 
        query: str
    ) -> Optional[str]:
        """Create a bulk operation for fetching large datasets."""
        mutation = """
        mutation bulkOperationRunQuery($query: String!) {
            bulkOperationRunQuery(query: $query) {
                bulkOperation {
                    id
                    status
                    createdAt
                    completedAt
                    objectCount
                    fileSize
                    url
                    partialDataUrl
                }
                userErrors {
                    field
                    message
                }
            }
        }
        """
        
        variables = {"query": query}
        
        url = f"{self._get_shop_url(shop)}/graphql.json"
        headers = self._get_headers(shop.access_token)
        
        payload = {
            "mutation": mutation,
            "variables": variables
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=payload, headers=headers)
                response.raise_for_status()
                
                data = response.json()
                if 'errors' in data:
                    return None
                
                bulk_operation = data.get('data', {}).get('bulkOperationRunQuery', {}).get('bulkOperation')
                if bulk_operation:
                    return bulk_operation.get('id')
                
                return None
            except Exception:
                return None
    
    async def get_bulk_operation_status(
        self, 
        shop: Shop, 
        operation_id: str
    ) -> Optional[Dict[str, Any]]:
        """Get status of a bulk operation."""
        query = """
        query getBulkOperation($id: ID!) {
            currentBulkOperation(id: $id) {
                id
                status
                createdAt
                completedAt
                objectCount
                fileSize
                url
                partialDataUrl
                errorCode
                errorMessage
            }
        }
        """
        
        variables = {"id": operation_id}
        
        url = f"{self._get_shop_url(shop)}/graphql.json"
        headers = self._get_headers(shop.access_token)
        
        payload = {
            "query": query,
            "variables": variables
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=payload, headers=headers)
                response.raise_for_status()
                
                data = response.json()
                if 'errors' in data:
                    return None
                
                return data.get('data', {}).get('currentBulkOperation')
            except Exception:
                return None
    
    async def register_webhooks(
        self, 
        shop: Shop, 
        webhook_url: str
    ) -> List[Dict[str, Any]]:
        """Register webhooks for the shop."""
        webhook_topics = [
            "orders/create",
            "orders/updated", 
            "orders/paid",
            "orders/cancelled",
            "orders/fulfilled",
            "orders/partially_fulfilled",
            "refunds/create",
            "transactions/create"
        ]
        
        created_webhooks = []
        
        for topic in webhook_topics:
            webhook_data = {
                "webhook": {
                    "topic": topic,
                    "address": f"{webhook_url}/webhooks/{topic.replace('/', '_')}",
                    "format": "json"
                }
            }
            
            url = f"{self._get_shop_url(shop)}/webhooks.json"
            headers = self._get_headers(shop.access_token)
            
            async with httpx.AsyncClient() as client:
                try:
                    response = await client.post(url, json=webhook_data, headers=headers)
                    response.raise_for_status()
                    
                    webhook = response.json().get('webhook')
                    if webhook:
                        created_webhooks.append(webhook)
                except Exception:
                    # Continue with other webhooks if one fails
                    continue
        
        return created_webhooks
    
    async def get_shop_info(self, shop: Shop) -> Optional[Dict[str, Any]]:
        """Get shop information."""
        query = """
        query getShop {
            shop {
                id
                name
                email
                currencyCode
                timezone
                plan {
                    displayName
                }
                myshopifyDomain
            }
        }
        """
        
        url = f"{self._get_shop_url(shop)}/graphql.json"
        headers = self._get_headers(shop.access_token)
        
        payload = {"query": query}
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=payload, headers=headers)
                response.raise_for_status()
                
                data = response.json()
                if 'errors' in data:
                    return None
                
                return data.get('data', {}).get('shop')
            except Exception:
                return None
