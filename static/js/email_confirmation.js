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
            order_items.push({
                'id': i.id,
                'quantity': i.quantity,
                })
            });
        document.getElementById('id_order_items')
        .setAttribute("value", JSON.stringify(order_items));    
        console.log(order_items)
    }
})();


 



