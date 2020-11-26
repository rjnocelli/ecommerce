console.log('email_confirmation.js working')
try{
    const order = JSON.parse(localStorage.getItem('order'))
    order_items = []
}catch (error){
    console.log(error)
}

const order = JSON.parse(localStorage.getItem('order'))

if(order && Object.keys(order).length > 0){
    Object.values(order).forEach((i) => {
        order_items.push({
            'id': i.id,
            'quantity': i.quantity,
            })
        });
    document.getElementById('id_order_items')
    .setAttribute("value", JSON.stringify(order_items));    
}   



