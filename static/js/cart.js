import { addLoQuieroTag, updateLocalStorage } from './functions.js'
console.log('cart.js working')

const addHtmlForItemQuantitySelection = (order_item_objs) => {
	const itemsDiv = document.getElementById('items-div');
	itemsDiv.innerHTML = ``
	for(var key in order_item_objs){
		itemsDiv.innerHTML += `
		<div id='item-row ${order_item_objs[key].id}' class='row'>
			<div class='col-lg-4'>
				<p style="display: inline-block;">${order_item_objs[key].name}</p><hr>
			</div>
			<div class='col-lg-4'>
				<p style="display: inline-block;">$${order_item_objs[key].price}</p><span></span>
			</div>
			<div class='col-lg-4'>
				<p id='cart-data'>
					<i id='minus-quantity ${order_item_objs[key].id}' class="fas fa-minus mr-1"></i>
					<span id='item-quantity ${order_item_objs[key].id}'>${order_item_objs[key].quantity}</span>
					<i id='plus-quantity ${order_item_objs[key].id}' class="fas fa-plus mr-1"></i>
					<i id='trash-can ${order_item_objs[key].id}' class="fa fa-trash ml-4" aria-hidden="true"></i>
				</p>
			<div class='col-lg-4'>
			</div>
			</div>
		</div>
		`
	};
};

buildProductsList()


    const updateCart = () =>{
        const cart = document.querySelector('#cart span')
        cart.innerHTML = ` `
        cart.innerHTML = ` ${localStorage.getItem('total_quantity')} `
    }

	function onOrderListFetched(order) {
			let order_item_objs = order
			let order_items_total_quantity = 0
			let order_items_total_price = 0

			localStorage.setItem('total_quantity', '0')
			localStorage.setItem('total_price', '0')

			function updateLocalStorage(){
				localStorage.setItem('order', JSON.stringify(order_item_objs))
				localStorage.setItem('total_quantity', JSON.stringify(order_items_total_quantity))
				localStorage.setItem('total_price', JSON.stringify(order_items_total_price))
			}

			addHtmlForItemQuantitySelection(order_item_objs);

			for(var key in order_item_objs){
				order_items_total_quantity += order_item_objs[key].quantity;
				order_items_total_price += order_item_objs[key].quantity * order_item_objs[key].price;
				localStorage.setItem('total_quantity', JSON.stringify(order_items_total_quantity))
				localStorage.setItem('total_price', JSON.stringify(order_items_total_price))
			};

			function renderTotalPriceAndQuantity(){
				const total = document.getElementById('total')
				total.innerHTML = ``
				total.innerHTML += `
				<h5>Cantidad Total: <span id='total-quantity'>${order_items_total_quantity}</span> unidades</h5>
				<h5>Precio Final: $ <span id='total-price'>${order_items_total_price}</span></h5>`
			}

			function deleteProduct(item) {
				const itemsDiv = document.getElementById('items-div')
				order_items_total_price -= item.price * item.quantity;
				order_items_total_quantity -= item.quantity;
				delete order_item_objs[item.name]
				updateLocalStorage()
				for(var i = 0; i < itemsDiv.children.length; i ++){
					if(itemsDiv.children[i].id === ('item-row ' + item.id)){
						itemsDiv.children[i].remove()}
					}
                    renderTotalPriceAndQuantity()
                    updateCart();

				}

			function substractQuantity(item) {
				const minus = document.getElementById('minus-quantity ' + JSON.stringify(item.id));
				if(item.quantity > 0){
					item.quantity -= 1;
					order_items_total_price -= parseInt(item.price);
					order_items_total_quantity -= 1;
					updateLocalStorage()
					if (item.quantity == 0) {
						minus.classList.add("disabled");
					}
					document.getElementById('item-quantity ' + item.id).innerHTML = item.quantity
					document.querySelector('#total-price').innerHTML = order_items_total_price
					document.querySelector('#total-quantity').innerHTML = order_items_total_quantity
				}
                renderTotalPriceAndQuantity()
                updateCart();
			};

			function addQuantity(item) {
				item.quantity += 1;
				const minus = document.getElementById('minus-quantity ' + item.id);
				if(item.quantity > 0){
					if(minus.classList.value.includes("disabled")){
						minus.classList.remove("disabled")
					}
					order_items_total_price += parseInt(item.price);
					order_items_total_quantity += 1;
                    updateLocalStorage();
                    updateCart();
				}

				document.getElementById('item-quantity ' + item.id).innerHTML = item.quantity
				document.querySelector('#total-price').innerHTML = order_items_total_price
				document.querySelector('#total-quantity').innerHTML = order_items_total_quantity
			}

			function callbackClosure(i, callback) {
			  return function() {
			    return callback(i);
			  }
			}

			for(var key in order_item_objs){
					const item_id = JSON.stringify(order_item_objs[key].id);
					const minus_id = 'minus-quantity ' + item_id;
					const minus = document.getElementById(minus_id);
					const plus_id = 'plus-quantity ' + item_id;
					const plus = document.getElementById(plus_id);
					const trash_can = document.getElementById("trash-can " + item_id)

					const item = order_item_objs[key]
					minus.addEventListener('click', callbackClosure(item, substractQuantity))
					plus.addEventListener('click', callbackClosure(item, addQuantity))
					trash_can.addEventListener('click', callbackClosure(item, deleteProduct))

			};

			renderTotalPriceAndQuantity()
		}

	function buildProductsList(){
		if(localStorage.getItem('order')){
			const order = localStorage.getItem('order')
			onOrderListFetched(JSON.parse(order))
		}else{
			alert('No hay orden creada. Agregue el primer producto al carro.')
		}
    }

const addProductOrCreateOrder = (product) => {
	console.log(product.name)
	if(localStorage.getItem('total_price') && localStorage.getItem('total_quantity')){
		total_quantity = parseInt(localStorage.getItem('total_quantity'))
		total_price = parseInt(localStorage.getItem('total_price'))
		console.log('ya existe orden, quantity y price')
	}else{
		total_quantity = 0
		total_price = 0
		console.log('creando variables')
	}
	if(localStorage.getItem('order')){
		order = JSON.parse(localStorage.getItem('order'))
			if(order[product.name]){
				order[product.name].quantity += 1 
			}else{
				order[product.name] = {'id':product.id,'name':product.name,'price':product.price,'quantity':1}
			}
	}else{
		order = {}
		order[product.name] = {'id':product.id,'name':product.name,'price':product.price,'quantity':1}
	}
total_quantity += 1
total_price += parseInt(product.price)
updateCart()
updateLocalStorage()
};
