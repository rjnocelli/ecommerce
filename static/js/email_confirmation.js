(function(){
    console.log('email_confirmation.js working')
    try{
        var order = JSON.parse(localStorage.getItem('order'))
        var order_items = []
    }catch(error){
        console.log(error)
    }

    if(order && Object.keys(order).length > 0){
        Object.values(order).forEach((i) => {
            console.log(i)
            order_items.push({
                'id': i.id,
                'product_name': i.name,
                'quantity': i.quantity,
                'sold_by_weight': i.sold_by_weight
                });
            });
        document.getElementById('id_order_items')
        .setAttribute("value", JSON.stringify(order_items));    
        console.log(order_items)
    }
})();


 



