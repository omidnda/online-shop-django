$(document).ready(
    function(){
        var urlParams = new URLSearchParams(window.location.search);
        if (urlParams==""){
            localStorage.clear();
        }
        $("input:ckeckbox").on("click", function(){
            var fav, favs=[];
            $("input:ckeckbox").each(function(){
                fav = {id: $(this).attr("Id"), value: $(this).prop("checked")};
                favs.push(fav);
            })
            localStorage.setItem("favorites", JSON.stringify(favs));
        })
        var favorites = JSON.parse(localStorage.getItem("favorites"));
        for (var i=0; i < favorites.lenght; i++){
            $("#"+ favorites[i].id).prop("checked", favorites[i].value);
        }
    }
);



function showVal(x){
    x= x.toString().replace(/\B(?=(\d{3}) + (?!\d))/g, ",");
    document.getElementById("sel-price").innerText = x;
};




function removeURLParameter(url, parameter){
    var urlparts = url.split("?");
    if(urlparts.lenght >= 2){
        var prefix = encodeURIComponent(parameter) + "=";
        var pars = urlparts[1].split(/[&;]/g);
        for (var i = pars.length; i-- > 0;) {    
            if (pars[i].lastIndexOf(prefix, 0) !== -1) {  
                pars.splice(i, 1);
            }
        }

        return urlparts[0] + (pars.length > 0 ? '?' + pars.join('&') : '');
    }
    return url;
};



status_of_shop_cart()

function status_of_shop_cart() {
    $.ajax({
        type : "GET",
        url : "/orders/status_of_shop_cart/",
    
        success : function (res) {
            $("#indicator__value").text(res);
        }
    });
};
//مرتب سازی
function selectSort(){
    var select_sort_value= $("#select_sort").val();
    var url = removeURLParameter(window.location.href,"sort_type");
    window.location = url + "&sort_type=" + select_sort_value;

};

function add_to_shop_cart(product_id,qty){
    if (qty===0) {
        qty=$("#input_qty").val()
    }
    $.ajax({
        type :"GET",
        url  : "/orders/add_to_shop_cart/",
        data : {
            product_id : product_id,
            qty : qty
        },
        success:function (res) {
            alert("کالای مورد نظر به سبد خرید شما اضافه شد")
            $("#indicator__value").text(res);
            status_of_shop_cart()
        }
    })
};

function delete_from_shop_cart(product_id) {
    $.ajax({
        type :"GET",
        url  : "/orders/delete_from_shop_cart/",
        data : {
            product_id : product_id,
        },
        success:function (res) {
            $("#shop_cart").html(res);
            status_of_shop_cart()
        }
    })
};

function update_shop_cart() {   
    var product_id_list = []
    var qty_list = []
    $("input[id^='qty_']").each(function(index){
        product_id_list.push($(this).attr('id').slice(4));
        qty_list.push($(this).val());
    });
    $.ajax({
        type : "GET",
        url : "/orders/update_shop_cart/",
        data : {
            product_id_list : product_id_list,
            qty_list : qty_list
        },
        success : function (res) {
            $("#shop_cart").html(res);
            status_of_shop_cart();
        }
    });
};
// -------------------------------------------------
// تابع برای ارسال نظر
function ShowCreateCommentForm(productId, commentId, slug) {
    $.ajax({
        type : "GET",
        url : "/comments/create_comment/" + slug,
        data : {
            productId:productId,
            commentId:commentId
        },
        success: function(res) {
            $("#btn_" + commentId).hide();
            $("#comment_form_" + commentId).html(res);
        }
    })
};


// امتیاز دهی به محصولات
function addScore(score, productId) {
    var starRatings = document.querySelectorAll(".fa-star");
    starRatings.forEach(element => {
        element.classList.remove("checked");
    });
    for(let i=1; i<=score; i++) {
        const element = document.getElementById("star_" + i);
        element.classList.add("checked");
    }

    $.ajax({
        type : "GET",
        url : "/scoring_favorite/add_score/",
        data : {
            productId:productId,
            score:score
        },
        success: function(res) {
           alert(res);
        }
    });
    starRatings.forEach(element => {
        element.classList.remove("disable");
    });
}
// --------------------------------------------
// اضافه کردن به علاقه مندی ها

function addToFavorite(productId) {
    $.ajax({
        type : "GET",
        url : "/scoring_favorite/add_to_favorite/",
        data : {
            productId:productId,
        },
        success: function(res) {
            // $("#favorite_value").html(res)
           alert(res);
        }
    });
};
// $(document).ready(function() {
//     $('.add-to-favorites').on('click', function(e) {
//         e.preventDefault();
//         const productID = $(this).data('product-id');
//         $.ajax({
//             type: 'POST',
//             url: `/scoring_favorite/add_to_favorite/${productId}/`,
//             success: function(response) {
//                 alert(response.message);
//                 // بروزرسانی وضعیت دکمه
//                 $(this).prop('disabled', true);
//             }.bind(this),
//             error: function(error) {
//                 alert('خطایی رخ داده است.');
//             }
//         });
//     });
// });

// -------------------------------------------------------------
// مقایسه کالاها

status_of_compare_list()

function status_of_compare_list() {
    
    $.ajax({
        type : "GET",
        url : "/products/status_of_compare_list/",

        success: function(res) {
          if(Number(res)===0){
            $("#compere_count_icon").hide();
          }else{
            $("#compere_count_icon").show();
            $("#compere_count").text(res);
          }
        }
    });
}
// اضافه کردن کالا به لیست مقایسه

function addToCompareList(productId, productGroupId) {
    $.ajax({
        type : "GET",
        url : "/products/add_to_compare_list/",
        data : {
            productId:productId,
            productGroupId:productGroupId
        },
        success: function(res) {
           alert(res);
           status_of_compare_list();
        }
    });
};

function deleteFromCompareList(productId) {
    $.ajax({
        type : "GET",
        url : "/products/delete_from_compare_list/",
        data : {
            productId:productId,
        },
        success: function(res) {
            $("#compare_list").html(res)
           status_of_compare_list();
        }
    });
}