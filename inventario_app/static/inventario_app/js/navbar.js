import { updateCart, updateLocalStorage, addProductOrCreateOrder } from './functions.js'

console.log('navbar.js working')

const addCartHtml = () => {
    let total_quantity = localStorage.getItem('total_quantity')
    if(total_quantity === null){
      total_quantity = '0'
    }
    document.getElementById('cart').innerHTML +=`
    <a class='candy-icon' href="/cart"><i class="far fa-candy-cane"><span> ${total_quantity} <span></i>
    </a> 
    `
  }

addCartHtml()

const form_submit_button = document.getElementById('search-submit')
const contacto_at = document.getElementById('contacto')

const products = JSON.parse(localStorage.getItem('products'))

contacto_at.addEventListener('click', (event) =>{
event.preventDefault();
window.scrollTo(0, document.body.scrollHeight);
});

const buildProductsListOnSearch = (query_params) => {
  const url = '/api/search/?q=' + query_params
  console.log(url)
  fetch(url)
    .then(function(response) { return response.json(); })
    .then(renderSearchResults);
  };
    
// const filterItems = (query) => {
// return products.filter(function(el) {
//     return ((el.name.toLowerCase().indexOf(query.toLowerCase()) > -1) 
//     || (el.description.toLowerCase().indexOf(query.toLowerCase()) > -1) 
//     || (el.category.map((i) => {return i.name.toLowerCase()}).join(" ").includes(query)));          
// })
// };

const renderSearchResults = (products) => {
    let query = ((document.getElementsByName('q')[0].value).split(" ")).join("+")
    console.log(query)
    window.history.pushState({'q':query}, 'Funes Dulceria', "search",);
    const base_div = document.getElementById('base-div');
    const title = `<div class='row'><h2>Resultado de la búsqueda "${query}"</h2></div>`
    const base_div_row = `<div class="row" id="base-div-row"></div>`
    base_div.innerHTML = title
    base_div.innerHTML += base_div_row
    const base_div_row_el = document.getElementById('base-div-row')
    console.log(products)
    if(products && products.length > 0){
    products.forEach((product) => {
        base_div_row_el.innerHTML += `
        <div class="col-lg-3 col-md-3 col-sm-3">
            <a href="product/${product.id}"><img id='img-atag ${product.id}' class="img-thumbnail" src=${product.image}></a>
            <div class="box-element product">
              <h6 class="pt-2" style="display: inline-block">${product.name.length > 20 ? product.name.slice(0,20).concat("...") : product.name}</h6>
                ${product.price ? `<h6>precio p/u: <span class='float-right'><strong>$ ${product.price}</strong></span></h6>` : `<h6>Producto Vendio Por Peso<h6/>`}
            </div>
            <br>
        </div>
        `
    });
    console.log('Productos', products)
    window.scrollTo(0,0)
    }else{console.log('no se ha encontrado ningun producto')};
};
          
const addEventListenerToBuscarButton = () => {
  form_submit_button.addEventListener('click', (e) => {
    e.preventDefault()
    let query = ((document.getElementsByName('q')[0].value).split(" ")).join("+")
    buildProductsListOnSearch(query)
    // let products_filtered = filterItems(query.toLowerCase())
    // renderSearchResults(products_filtered)
  });
};

addEventListenerToBuscarButton()

// --------- Fetch all categories -------
const displayCatsOnNavbar = (response) => {
  const cats_div = document.getElementById('dropdown-cats-list')
  response.forEach((cat)=>{
    const node = `<a id='cat ${cat.id}' class="dropdown-item" href="">${cat.name}</a>`
    cats_div.insertAdjacentHTML('afterbegin', node)
    document.getElementById('cat ' + cat.id).addEventListener('click', (e)=>{
      e.preventDefault()
      const query = cat.name.toLowerCase()
      let products_filtered = filterItems(query)
      console.log(products_filtered)
      renderSearchResults(products_filtered, query)
    });
  });
};

const buildCategoriesList = () => {
  const url = '/api/categories-list/'

  fetch(url)
      .then(function(response) { return response.json(); })
      .then(displayCatsOnNavbar);
  }
  buildCategoriesList()


const renderIndex = () => {
  let base_div = document.getElementById('base-div');
  console.log(base_div)
  base_div = ``
  base_div.insertAdjacentHTML('afterbegin',
  `<div id='jumbotron' style='background-color:#abb7b7' class="jumbotron text-center expand">
    <h1 class="">Bienvenidos a Funes Dulceria</h1>
    <p class="lead text-muted">Elegí lo que quieras y te lo enviamos a tu casa<p>
  </div>
  <div id='most-popular-container' style="padding: 10px" class="row shadow-lg border boder-light">
    <div id='most-popular-row' class="row"></div> 
    </div><hr>
  <div id='product-details' class="row"></div>
  `) 
};