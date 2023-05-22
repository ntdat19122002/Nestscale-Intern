<template>
    <div class="title">
        {{bundle_title}}
    </div>
    <div class="tier-bundle-item">
        <div class="tier-img">
            <img v-if="product_image" :src="'data:image/png;base64,'+product_image" alt="Product Image">
            <img v-else src='/bundle/static/images/product/default.png' alt="Product Image">
        </div>
        <div>
            <div class="title">{{ product_name }}</div>
            <div class="range-list">
                <div class="range-list-item" v-for="qty in qtys" :key="qty" @click="addToCart(product_id,qty.start)">
                    <div class="title-range">Add {{qty.start}}<span v-if="qty.end">-{{qty.end}}</span> items</div>
                    <div class="value-discount">Get {{qty.discount_value}}% off</div>
                    <div v-if="qty.highlight_enable" class="highlight">Most Popular</div>
                    <span v-if="qty.num"> x {{ qty.num }}</span>
                </div>
                
            </div>
        </div>
    </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router';
export default {
    props:['product_image','product_id','product_name','bundle_tier','bundle_title','qtys','num'],
    setup(props){
        const router = useRouter()
        const product_image = ref(props.product_image);
        const product_id = ref(props.product_id);
        const product_name = ref(props.product_name);
        const bundle_title = ref(props.bundle_title)
        const qtys = ref(props.qtys)
        const num = ref(props.num)

        const addToCart = async (id, quantity) => {
            await fetch('https://odoo.website/add-to-cart', {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ 'params':{"id": id ,"quantity":quantity}})
            })
            router.push({name:'cart'})
            location.reload()
        }
        
        return {product_image,product_id,product_name,bundle_title,qtys,addToCart,num}
    }
}
</script>

<style>
.tier-bundle{
    border-top: 1px solid rgb(177, 177, 177);
    padding: 10px;
}
.tier-bundle>.title{
    font-size: 24px;
    font-weight: 600;
    color: #494848;
    margin-bottom: 20px;
}
.tier-bundle-item{
    display: flex;
}
.tier-bundle-item img{
    width: 50px;
    height: 40px;
    margin: 10px 30px 0 10px;
}
.tier-bundle-item .title{
    color: rgb(198, 76, 32);
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 20px;
}
.range-list{
    display: flex;
    text-align: center;
    flex-wrap: wrap;
}
.range-list-item{
    height: max-content;
    border: 1px solid #b6b6b6;
    border-radius: 6px;
    margin-right: 30px;
    margin-bottom: 10px;
}

.range-list-item .title-range{
    background: #4a393a;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    color: white;
    padding: 10px;
    font-weight: 600;
}

.highlight{
    background: #4a393a;
    border-radius: 4px;
    margin: 0 8px 4px;
    color: white;
    padding: 2px;
    font-size: 12px;
    font-weight: bold;
}
.range-list-item .value-discount{
    padding: 15px 0;
    font-weight: 550;
    color: #494848;
}
</style>