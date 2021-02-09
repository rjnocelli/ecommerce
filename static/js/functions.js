export const addLoQuieroTag = (products, first_half_id) =>{
    console.log('addLoQuieroTag funciona')
    const candy_cane = document.getElementsByClassName('candy-icon')[0]
    console.log(candy_cane, candy_cane.classList)
    candy_cane.classList.toggle('candy-cane-animation')
    let lo_quiero_atag, product
    if(products.length > 1){
        products.forEach((product) => {
            lo_quiero_atag = document.getElementById(`${first_half_id} ${product.id}`)
            lo_quiero_atag.addEventListener('click', (event) => {
                event.preventDefault()
                addProductOrCreateOrder(product)
            });
        });
    
    }else if(products.length === 1){
        product = products[0]
            lo_quiero_atag = document.getElementById(`${first_half_id} ${product.id}`)
            lo_quiero_atag.addEventListener('click', (event) => {
                event.preventDefault()
                addProductOrCreateOrder(product)
            });
    }else{
        product = products
            lo_quiero_atag = document.getElementById(`${first_half_id} ${product.id}`)
            lo_quiero_atag.addEventListener('click', (event) => {
                event.preventDefault()
                addProductOrCreateOrder(product)
            });
    }
};

export const toggleClassAnimationButton = () => {
    const cart = document.getElementsByClassName('candy-icon')[0].firstChild
    if(cart.classList.contains('scale')){
        cart.classList.toggle('scale');
        cart.classList.toggle('scale2');
    }else if(cart.classList.contains('scale2')){
        cart.classList.add('scale');
        cart.classList.toggle('scale2');
    }else{
        cart.classList.add('scale');
    }
};

export const addProductOrCreateOrder = (product) => {
    const product_name = product.name
    const cart = document.getElementsByClassName('candy-icon')[0].firstChild

    toggleClassAnimationButton()

    if(product.sold_by_weight){
        console.log('PRODUCT SOLD BY WEIGHT!')
        const weight_and_price = document.getElementById('price-by-weight-select-id').value.split(" ")
        product.price = JSON.parse(weight_and_price[1])
        product.name = product.name + " " + weight_and_price[0]
    }
    let total_quantity = 0, total_price = 60, order
    if(localStorage.getItem('total_price') && localStorage.getItem('total_quantity')){
        total_quantity = parseInt(localStorage.getItem('total_quantity'))
        total_price = parseInt(localStorage.getItem('total_price'))
        console.log('ya existe orden, quantity y price')
    }
    total_quantity += 1
    total_price += parseInt(product.price)

    if(localStorage.getItem('order')){
        order = JSON.parse(localStorage.getItem('order'))
            if(order[product.name]){
                order[product.name].quantity += 1 
            }else{
                order[product.name] = {'id':product.id,'name':product.name,'price':product.price,'quantity':1}
                if(product.sold_by_weight){
                    order[product.name].sold_by_weight = "true " + product.name.split(" ")[product.name.split(" ").length-1]}
                    else{
                        order[product.name].sold_by_weight = false
                    }
            }
    }else{
        order = {}
        order[product.name] = {'id':product.id,'name':product.name,'price':product.price,'quantity':1}     
        if(product.sold_by_weight){
            order[product.name].sold_by_weight = "true " + product.name.split(" ")[product.name.split(" ").length-1]}else{
                order[product.name].sold_by_weight = false
            }
   }
   
   product.name = product_name
    updateLocalStorage(order, total_price, total_quantity)
    updateCart(total_quantity)
};

export const updateCart = (total_quantity) => {
    const cart = document.querySelector('#cart span')
    cart.innerHTML = ` `
    cart.innerHTML = ` ${total_quantity} `
}
export const updateLocalStorage = (order, total_price, total_quantity) => {
        console.log('updating local storage', total_quantity, total_price)
        localStorage.setItem('order', JSON.stringify(order))
        localStorage.setItem('total_quantity', JSON.stringify(total_quantity))
        localStorage.setItem('total_price', JSON.stringify(total_price))
    }

export const callbackClosure = (i, callback) => {
    return function() {
    return callback(i);
    }
}