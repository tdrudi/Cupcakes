const BASE_API_URL = "http://127.0.0.1:5000/api"


/*Get info about a cupcake */
function getCupcakeHTML(cupcake){
    return `<div id="${cupcake.id}">
            <li>
            ${cupcake.flavor}.......${cupcake.size}.......${cupcake.rating}
            <button id=delete> x </button>
            </li>
            <img src="${cupcake.image}" height=150 width=150>
            </div>`;

}

/*Show all cupcakes*/
async function showAllCupcakes(){
    const response = await axios.get(`${BASE_API_URL}/cupcakes`);

    /*Show cupcakes*/
    for(let info of response.data.cupcakes){
        let newCupcake =$(getCupcakeHTML(info));
        $("#show_cupcakes").append(newCupcake);
    }

    /*Form for adding new cupcakes*/
    $("#new_cupcake").on("submit", async function(e){
        e.preventDefault();

        let flavor = $("#flavor").val();
        let size = $("#size").val();
        let rating = $("#rating").val();
        let image = $("#image").val();
        
        const res = await axios.post(`${BASE_API_URL}/cupcakes`, 
        {flavor, rating, size, image});
        
        let newCupcake = $(getCupcakeHTML(res.data.cupcake));
        $("#show_cupcakes").append(newCupcake);
        $("#new_cupcake").trigger("reset");

    });
}

$("#show_cupcakes").on("click", "#delete", async function(e){
    /*Delete a cupcake when click delete button */
    e.preventDefault();
    let $cupcake = $(e.target).closest("div");
    let cupcakeId = $cupcake.attr("id");

    await axios.delete(`${BASE_API_URL}/cupcakes/${cupcakeId}`)
    $cupcake.remove();
});

$(showAllCupcakes);

