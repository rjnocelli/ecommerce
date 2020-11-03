order = JSON.parse(localStorage.getItem('order'))
    console.log(order)

    final_order = {
        "complete": false,
        "active": true,
        "customer_name": " ",
        "customer_email": " ",
        "items": [],
    }

    Object.values(order).forEach((i) =>{
        final_order.items.push(
                i.id,
            );
        });
    
    console.log('final order', final_order)

    const form = document.getElementById('form')
    const csrftoken = form.getElementsByTagName('input')[0].value

    
    function createOrderItem(order){
        
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
        const name = form.getElementsByTagName('input')[1].value
        const last_name = form.getElementsByTagName('input')[2].value
        const email = form.getElementsByTagName('input')[3].value
        final_order.customer_name = `${name} ${last_name}`
        final_order.customer_email = email

        
        createOrderItem(final_order)
    });