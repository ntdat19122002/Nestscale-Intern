<template>
  <header>
    <div class="menu">
      
      <div class="navbar">
        <div class="logo">
          <router-link :to="{name:'home'}"><img src="/bundle/static/images/logo/logo.png" alt="asdf"></router-link>
        </div>
        <ul>
          <li class="nav-item"><router-link :to="{name:'home'}">Home</router-link></li>
          <li class="nav-item"><router-link :to="{name:'shopPage',params:{page:1}}">Shop</router-link></li>
          <li class="nav-item"><router-link :to="{name:'contact'}">Contact Us</router-link></li>
          <li class="nav-item">
            <router-link :to="{name:'cart'}">
              <i class="fa fa-shopping-cart"></i>
              <span class="count-item mini-button">{{length_cart}}</span>
            </router-link>
          </li>
        </ul>
      </div>
      <div class="contact">
        <li class="nav-item"><strong>Mitchel Admin</strong></li>
        <router-link class="button mini-button" :to="{name:'contact'}">Contact us</router-link>
      </div>
    </div>
  </header>
</template>

<script>
import { ref } from 'vue'
export default {
  setup(){
    const length_cart = ref(0)
    const load = async () => {
      length_cart.value  = await fetch('https://odoo.website/length-cart')
                        .then(res => res.json())
                        .then(data => data.length)
    }
    load()
    return {length_cart}
  }
}
</script>


<style scoped>
  header{
    height: 56px;
    padding: 8px 16px;
    box-shadow: 0 0.125rem 0.25rem rgb(0 0 0 / 8%) !important;
  }

  header .menu{
    display: flex;
    margin: 0 20%;
    justify-content: space-between;
  }

  .menu .logo img{
    margin-right: 24px;
  }

  .menu .navbar{
    display: flex;
    justify-items: center;
    align-items: center;
  }

  .menu .navbar ul{
    display: flex;
  }

  .navbar .nav-item{
    padding: 8px;
  }

  .navbar .nav-item:nth-child(5){
    margin: 0 16px;
  }
  .navbar .count-item{
    position: absolute;
    font-size: 13px;
    padding: 4px;
    top: 12px;
    margin-left: 2px;
  }

  .navbar .nav-item a{
    color: rgba(0, 0, 0, 0.5);
  }


  .menu .contact{
      float: right;
      display: flex;
      align-items: center;
  }

  .contact a{
      margin-left: 24px;
      padding: 10px 12px;
  }

  .navbar .router-link-active{
    color: rgb(35, 35, 35) !important;
  }
</style>
