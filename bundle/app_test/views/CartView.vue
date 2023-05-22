<template>
  <div class="cart">
    <div class="cart-status">
      <hr>
      <div class="item-status">
        <input type="radio" name="" id="">
        <div>Review order</div>
      </div>
      <div class="item-status">
        <input type="radio" name="" id="">
        <div>Address</div>
      </div>
      <div class="item-status">
        <input type="radio" name="" id="">
        <div>Confirm order</div>
      </div>
    </div>
    <div class="oder-process">
      <div class="cart-list">
        <div v-if="cart_lines && cart_lines.length>0"> 
          <div class="cart-list-header">
            <div class="product">
              Product
            </div>
            <div class="quantity">
              Quantity
            </div>
            <div class="price">
              Price
            </div>
          </div>
          <div class="cart-list-item" v-for="cart_line in cart_lines" :key="cart_line">
            <div class="product">
              <img v-if="cart_line.product.image" :src="'data:image/png;base64,'+ cart_line.product.image" alt="Product Image">
              <img v-else src='/bundle/static/images/product/default.png' alt="Product Image">
              {{ cart_line.product.name }}
            </div>
            <div class="quantity">
              <div class="change-quantity-btn" @click="reduceQuantity(cart_line)">-</div>
              <input @change="changeQuantity(cart_line.id,cart_line.quantity)" type="number" v-model="cart_line.quantity">
              <div class="change-quantity-btn" @click="addQuantity(cart_line)">+</div>
            </div>
            <div class="price">
              $ {{ cart_line.product.price }}
            </div>
            <div @click="deleteCartLine(cart_line.id)" class="delete">
              <i class="fa-solid fa-trash"></i>
            </div>
          </div>
        </div>
        <div v-else>
          You haven't bought any product
        </div>

        <div class="cart-list-btn">
          <div class="pp-button"><router-link :to="{name:'shopPage',params:{page:1}}">Continue Shopping</router-link></div>
          <div class="mini-button"><router-link :to="{name:'shopPage',params:{page:1}}">Process Checkout</router-link></div>
        </div>

        <!-- bundle discount -->
          <div class="bundle" v-if="bundles && bundles.bundle_total">
            <MultipleBundle :bundle_total='bundles.bundle_total' :bundle_each="bundles.bundle_each"/>
            <div v-for="bundle in bundles.bundle_tier" :key="bundle">
              <div v-for="product in bundle.product" :key="product" class="tier-bundle">
                <TierBundle 
                  :product_image="product.image" 
                  :product_id="product.id" 
                  :product_name="product.name" 
                  :bundle_title="bundle.title"
                  :qtys="product.qty"
                /> 
              </div>
            </div>
            
          </div>
      </div>

      <!-- Cart Total -->
      <div class="cart-order">
        <div class="title">
          Order Total
        </div>
        <div class="subtotal row-order">
          <div>
            Subtotal:
          </div>
          <div>
            $ {{ total }}
          </div>
        </div>
        <div class="taxes row-order">
          <div>
            Discount:
          </div>
          <div>
            $ {{ discount_total }}
          </div>
        </div>
        <div class="total row-order">
          <div>
            Total:
          </div>
          <div>
            $ {{ total - discount_total}}
          </div>
        </div>
        <div class="promotion-code">
          I have a promo code
        </div>
        <div class="checkout-btn">
          <span class="pp-button">Process Checkout</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, watch } from 'vue'
import MultipleBundle from '../components/MultipleBundle.vue'
import TierBundle from '../components/TierBundle.vue'
export default {
  components: { MultipleBundle, TierBundle },
   setup(props){
    const cart_lines = ref(null)
    const bundles = ref(null)
    const total = ref(0)
    const discount_total = ref(0)
    const load = async ()=>{
      try{
        let data = await fetch('https://odoo.website/cart')
                          .then(res => res.json())
        cart_lines.value = data.cart_lines
        bundles.value = data.bundles
        total.value = data.total
        discount_total.value = data.discount_total.toFixed(2)
      }
      catch(err){
        console.log(err.meassage);
      }
    }
    load()

    const deleteCartLine = async (id) => {
      try{
        await fetch('https://odoo.website/delete-cart-line/'+id)
        load()
      }
      catch(err){
        console.log(err.meassage);
      }
    }

    const reduceQuantity = (cart_line) => {
      changeQuantity(cart_line.id,--cart_line.quantity)
    }

    const addQuantity = (cart_line) => {
      changeQuantity(cart_line.id,++cart_line.quantity)
    }

    const changeQuantity = async(id,quantity) => {
      if(quantity<=0){
        deleteCartLine(id)
        load()
      }
      else{
        await fetch('https://odoo.website/update-cart-line/'+id+'/quantity/'+quantity)
        .catch(err=>{
          console.log(err);
        })
        load()
      }
    }
    return {load,cart_lines,bundles,discount_total,total,deleteCartLine,changeQuantity,reduceQuantity,addQuantity}
  }
}
</script>

<style scoped>
  .cart{
    padding: 10px 20%;
  }
  .cart-status{
    position: relative;
    margin: 30px 30px 80px;
  }
  .item-status{
    position: absolute;
    top:-7.5px;
    text-align: center;
  }
  .item-status:nth-of-type(1){
    left: 15%;
  }
  .item-status:nth-of-type(2){
    left: 45%;
  }
  .item-status:nth-of-type(3){
    left: 75%;
  }

  .oder-process{
    margin: 30px 0;
    display: flex;
  }
  .cart-list{
    margin-right: 30px;
    border-top: 1px solid #999;
    width:70%;
  }
  .cart-list-header{
    display: flex;
    font-weight: bold;
    padding: 10px;
    border-bottom: 2px solid #585858;
  }
  .cart-list-header .quantity{
    transform: translateX(-13px);
  }
  .cart-list-header .quantity, .cart-list-header .price{
    display: flex;
    justify-content: center;
  }
  .cart-list-item{
    padding: 10px 0;
    display: flex;
  }
  .row-order{
    display: flex;
    margin: 10px 0;
    padding: 10px 0;
  }
  .row-order>div{
    width: 50%;
    text-align: end;
  }
  .cart-list .cart-list-item:nth-of-type(even){
    background: rgba(0, 0, 0, 0.05);
  }
  .total{
    border-top: 1px solid #000;
    font-weight: bold;
  }

  .cart-list-btn{
    margin-top: 20px;
    display: flex;
    justify-content:space-between;
  }
  .cart-order{
    height: fit-content;
    width: 30%;
    border: 1px solid #999;
    padding: 20px;
  }

  .cart-order .title{
    font-size: 25px;
    padding-bottom: 20px;
    border-bottom: 1px solid #999;
  }

   a{
    color: white;
  }

  .product{
    width: 50%;
    display: flex;
  }

  .product img{
    width: 60px;
    height: 40px;
    margin: 0 10px;
  }
  .quantity{
    display: flex;
    width: 25%;
    text-align: center;
  }

  .quantity .change-quantity-btn{
    font-size: 28px;
    display: flex;
    align-items: center;
  }
  
  .quantity .change-quantity-btn:nth-child(1){
    font-size: 34px;
  }

  .quantity input{
    margin: 0 10px;
    font-size: 14px;
    width: 60%;
    text-align: center;
  }
  .price{
    width: 20%;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .delete{
    width: 5%;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .promotion-code{
    text-align: end;
  }

  .checkout-btn{
    margin-top: 30px;
    display: flex;
    justify-content: flex-end;
  }

  .bundle{
    margin-top: 20px;
    float: right;
    width: 60%;
  }
</style>