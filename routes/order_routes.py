from fastapi import APIRouter, HTTPException, Depends
from configs.database import order_collection, product_collection, cart_collection
from models.order_models import Order
from bson import ObjectId
from utils.auth_dependencies import get_current_user, admin_required


router = APIRouter()


# Place Order 
@router.post("/orders")
def place_order(order: Order, current_user: dict = Depends(get_current_user)):
    
    if str(current_user["_id"]) != order.user_id and current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
        
        
    # 1. Decrease stock for each product
    for product_id in order.products:
        # Convert string to ObjectId
        obj_id = ObjectId(product_id)

        # Check if product exists
        product = product_collection.find_one({"_id": obj_id})
        if not product:
            raise HTTPException(status_code=404, detail=f"Product with ID {product_id} not found")

        # Check stock
        if product.get("stock", 0) <= 0:
            raise HTTPException(status_code=400, detail=f"Product '{product.get('name')}' is out of stock")

        # Decrease stock by 1
        product_collection.update_one(
            {"_id": obj_id},
            {"$inc": {"stock": -1}}
        )

    # 2. Insert the order
    res = order_collection.insert_one(order.model_dump())

    # 3. Clear user's cart items after successful order creation
    cart_collection.update_one({"user_id": order.user_id}, {"$set": {"items": []}})

    return {
        "success": res.acknowledged,
        "message": "Order Created Successfully",
        "order_id": str(res.inserted_id)
    }

# Get all orders
@router.get("/orders")
def get_orders(current_user: dict = Depends(admin_required)):
    orders_cursor = order_collection.find()
    
    orders = []
    for order in orders_cursor:
        order["id"] = str(order["_id"])
        del order["_id"]
        orders.append(order)
        
    return orders


# Get Order Detail
@router.get("/orders/{id}")
def get_order_by_id(id: str, current_user: dict = Depends(get_current_user)):
    order = order_collection.find_one({"_id": ObjectId(id)})
    
    if not order:
        raise HTTPException(status_code=404, detail="Order Not Found")
    
    order["id"] = str(order["_id"])
    
    del order["_id"]
    
    return order

# Update Order Status (Admin)
@router.put("/admin/orders/{id}/status")
def update_order_status(id: str, status: str, current_user: dict = Depends(admin_required)):
    """
    Update the status of an existing order. Allowed statuses:
    Pending, Confirmed, Shipped, Delivered, Cancelled
    """
    allowed_statuses = ["Pending", "Confirmed", "Shipped", "Delivered", "Cancelled"]
    if status not in allowed_statuses:
        raise HTTPException(status_code=400, detail="Invalid status")

    result = order_collection.update_one({"_id": ObjectId(id)}, {"$set": {"status": status}})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Order Not Found")

    return {"message": f"Order status updated to {status}", "order_id": id, "status": status}

# Get Orders by user id (Order History)
@router.get("/orders/user/{user_id}")
def get_orders_by_user(user_id : str, current_user: dict = Depends(get_current_user)):
    
    if str(current_user["_id"]) != user_id and current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    orders_cursor = order_collection.find({"user_id": user_id})
    
    orders = []
    
    for order in orders_cursor:
        order["id"] = str(order["_id"])
        
        del order["_id"]
        
    return orders


 