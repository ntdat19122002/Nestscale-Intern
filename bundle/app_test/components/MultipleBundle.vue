<template>
    <div class="multiple-bundle" v-for="bundle in bundle_total" :key="bundle">
        <div class="title">
            {{bundle.title}} <span v-if="bundle.quantity">x {{bundle.quantity}}</span>
        </div>
        <div class="multiple-bundle-item" v-for="product in bundle.products" :key="product">
            <div>
                <img :src="'data:image/png;base64,'+product.image" alt="Product">
                <div class="item-title">
                    {{product.name}}
                </div>
            </div>
            <div v-if="bundle.discount_type!='total_fix' || bundle.discount_type!='hard_fix'">
                <div class="original-price">${{product.price}}</div>
                <div class="price-after">${{product.price_after}}</div>
            </div>
        </div>
        <div class="add-bundle">
            <div class="bundle-price">
                Total <span class="price-after">${{ bundle.sale_total}}</span> <span class="original-price">${{ bundle.total }}</span>
            </div>
            <button class="add-bundle-button" @click='addBundleToCart(bundle.id)'>
                ADD BUNDLE
            </button>
        </div>
    </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
export default {
    props:['bundle_total','bundle_each'],
    setup(props){
        const router = useRouter()
        const bundle_total = ref(props.bundle_total)
        const bundle_each = ref(props.bundle_each)
        bundle_total.value = bundle_total.value.concat(bundle_each.value)

        const addBundleToCart = async (id) =>{
            await fetch('https://odoo.website/add-bundle-to-cart/'+id)
            router.push({name:'cart'})
            location.reload()
        }
        return {bundle_total,addBundleToCart}
    }
}
</script>

<style scoped>
    .multiple-bundle{
        border-top: 1px solid rgb(177, 177, 177);
        padding: 10px;
    }
    .multiple-bundle .title{
        font-size: 24px;
        font-weight: 600;
        color: #494848;
        margin-bottom: 20px;
    }
    .multiple-bundle-item{
        padding: 10px 0;
        display: flex;
        justify-content: space-between;
        border-bottom: 1px solid #d6d6d6;
    }
    .multiple-bundle-item div:nth-child(1){
        display: flex;
    }
    .multiple-bundle-item img{
        margin: 10px;
        width: 50px;
        height: 40px;
    }

    .multiple-bundle-item .item-title{
        color: #df000f;
        font-weight: 600;
    }

    .original-price{
        color: #d00000;
        text-decoration: line-through;
        font-weight: 500;
    }

    .price-after{
        color:#38cd6c;
        font-size: 18px;
        font-weight: 500;
    }

    .add-bundle{
        margin: 20px 0;
        display: flex;
        justify-content: space-between;
    }
    .add-bundle-button{
        padding: 15px 60px;
        background: #00dd4d;
        border-radius: 6px;
        font-weight: 700;
        color: white;
        border: none;
    }
</style>