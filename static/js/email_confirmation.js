order = JSON.parse(localStorage.getItem('order'))

final_order = {
    "complete": false,
    "active": true,
    "customer_name": " ",
    "customer_email": " ",
    "items": [],
}

Object.values(order).forEach((i) =>{
    console.log("item", i)
    final_order.items.push({
        'id': i.id,
        'quantity': i.quantity,
        })
    });

console.log('final order', final_order)

const form = document.getElementById('form')
const csrftoken = form.getElementsByTagName('input')[0].value


function createOrderItem(order){
    console.log('Esta es la funcion createOrderItem')

    const url = '/api/order-create/'

	fetch(url, {
        method: 'POST',
        body: JSON.stringify(final_order),
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        }
    }).then(res => res.json())
    .catch(error => console.error('Error', error))
    .then(response => console.log('Success', response));

}
document.getElementById('enviar-button').addEventListener('click', (event) => {
    if(JSON.parse(localStorage.getItem('total_quantity')) >0 ){
        const name = form.getElementsByTagName('input')[1].value
        const last_name = form.getElementsByTagName('input')[2].value
        const email = form.getElementsByTagName('input')[3].value
        final_order.customer_name = `${name} ${last_name}`
        final_order.customer_email = email
        createOrderItem(final_order)
    }else{
        event.preventDefault()
        let message = document.querySelector('#order-empty-message')
        message.classList.add('show')
        console.log('la orden esta vacia')
    }
});