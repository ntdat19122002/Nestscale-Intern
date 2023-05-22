<template>
    <Header/>

  <RouterView />

  <Footer></Footer>
</template>

<script>

import { RouterView } from 'vue-router'
import Footer from "./components/Footer.vue";
import Header from "./components/Header.vue";

export default {
    name: "App",
    components: {Header, Footer},
    computed: {
        url(){
            return this.$store.state.url
        }
    }
}
</script>