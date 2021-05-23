import { addLoQuieroTag, updateLocalStorage, callbackClosure, toggleClassAnimationButton } from './functions.js'
console.log('cart.js working')

const addHtmlForItemQuantitySelection = (order_item_objs) => {
	const itemsDiv = document.getElementById('items-div');
	itemsDiv.innerHTML = ``
	for(var key in order_item_objs){
		itemsDiv.innerHTML += `
		<div id='item-row ${order_item_objs[key].name} ${order_item_objs[key].id}' class='row'>
			<div class='col-4 col-lg-4 col-sm-4'>
				<p style="display: inline-block;">${order_item_objs[key].name}</p><hr>
			</div>
			<div class='col-4 col-lg-4 col-sm-4'>
				<p style="display: inline-block;">$${order_item_objs[key].price}</p><span></span>
			</div>
			<div class='col-4 col-lg-4 col-sm-4'>
				<p id='cart-data'>
					<i id='minus-quantity ${order_item_objs[key].name} ${order_item_objs[key].id}' class="fas fa-minus mr-1"></i>
					<span id='item-quantity ${order_item_objs[key].name} ${order_item_objs[key].id}'>${order_item_objs[key].quantity}</span>
					<i id='plus-quantity ${order_item_objs[key].name} ${order_item_objs[key].id}' class="fas fa-plus mr-1"></i>
					<i id='trash-can ${order_item_objs[key].name} ${order_item_objs[key].id}' class="fa fa-trash ml-2" aria-hidden="true"></i>
				</p>
			<div class='col-4 col-lg-4 col-sm-4'>
			</div>
			</div>
		</div>
		`
	};
	itemsDiv.innerHTML += `
	<div class='row'>
		<div class='col-4 col-lg-4 col-sm-4'>
			<p style="display: inline-block;">Envio</p><hr>
		</div>
		<div class='col-4 col-lg-4 col-sm-4'>
			<p style="display: inline-block;">$ 80</p>
		</div>
	</div>`
};

const renderTotalPriceAndQuantity = (order_items_total_quantity, order_items_total_price) => {
	const total = document.getElementById('total')
	total.innerHTML = ``
	total.innerHTML += `
	<h5>Cantidad Total: <span id='total-quantity'>${order_items_total_quantity}</span> unidades</h5>
	<h5>Precio Final: $ <span id='total-price'>${order_items_total_price}</span></h5>`
}

const updateCart = () =>{
	const cart = document.querySelector('#cart span')
	cart.innerHTML = ` `
	cart.innerHTML = ` ${localStorage.getItem('total_quantity')} `
}

const onOrderListFetched = (order) => {

		let order_item_objs = order
		let order_items_total_price = 80
		let order_items_total_quantity = 0
		
		localStorage.setItem('total_quantity', '0')
		localStorage.setItem('total_price', '0')

		renderTotalPriceAndQuantity(order_items_total_quantity, order_items_total_price)
		addHtmlForItemQuantitySelection(order_item_objs);

		for(var key in order_item_objs){
			order_items_total_quantity += order_item_objs[key].quantity;
			order_items_total_price += order_item_objs[key].quantity * order_item_objs[key].price;
			localStorage.setItem('total_quantity', JSON.stringify(order_items_total_quantity))
			localStorage.setItem('total_price', JSON.stringify(order_items_total_price))
		};

		const deleteProduct = (item) => {

			toggleClassAnimationButton()

			const itemsDiv = document.getElementById('items-div')
				order_items_total_price -= item.price * item.quantity;
				order_items_total_quantity -= item.quantity;
				delete order_item_objs[item.name]
				updateLocalStorage(order_item_objs, order_items_total_price, order_items_total_quantity)
			for(var i = 0; i < itemsDiv.children.length; i ++){
				if(itemsDiv.children[i].id === ('item-row ' + item.name + ' ' + item.id)){
					itemsDiv.children[i].remove()}
				}
				renderTotalPriceAndQuantity(order_items_total_quantity, order_items_total_price)
				updateCart();

			}

		const substractQuantity = (item) => {

			toggleClassAnimationButton()

			const minus = document.getElementById('minus-quantity ' + item.name + ' ' + item.id);
			if(item.quantity > 0){
				console.log(minus)

				item.quantity -= 1;
				order_items_total_price -= parseInt(item.price);
				order_items_total_quantity -= 1;
				updateLocalStorage(order_item_objs, order_items_total_price, order_items_total_quantity)
				if (item.quantity == 0) {
					minus.classList.add("disabled");
				}
				document.getElementById('item-quantity ' + item.name + ' ' + item.id).innerHTML = item.quantity
				document.querySelector('#total-price').innerHTML = order_items_total_price
				document.querySelector('#total-quantity').innerHTML = order_items_total_quantity
			}
			renderTotalPriceAndQuantity(order_items_total_quantity, order_items_total_price)
			updateCart();
		};

		const addQuantity = (item) => {

			toggleClassAnimationButton()

			item.quantity += 1;
			const minus = document.getElementById('minus-quantity ' + item.name + ' ' + item.id);
			if(item.quantity > 0){
				if(minus.classList.value.includes("disabled")){
					minus.classList.remove("disabled")
				}
				order_items_total_price += parseInt(item.price);
				order_items_total_quantity += 1;
				updateLocalStorage(order_item_objs, order_items_total_price, order_items_total_quantity);
				updateCart();
			}

			document.getElementById('item-quantity ' + item.name + ' ' + item.id).innerHTML = item.quantity
			document.querySelector('#total-price').innerHTML = order_items_total_price
			document.querySelector('#total-quantity').innerHTML = order_items_total_quantity
		}

		for(var key in order_item_objs){
				const item_id = order_item_objs[key].name + ' ' + order_item_objs[key].id;
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

		renderTotalPriceAndQuantity(order_items_total_quantity, order_items_total_price)
	}

const buildProductsList = () => {
	if(localStorage.getItem('order')){
		const order = localStorage.getItem('order')
		onOrderListFetched(JSON.parse(order))
	}else{
		alert('No hay orden creada. Agregue el primer producto al carro.')
	}
}

buildProductsList()

