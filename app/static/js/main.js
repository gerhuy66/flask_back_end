


async function searchCv()
{
    
    let searchFilter = $("#filterSelect").val();
    let searchValue = $("#search").val();

    let ro = {
        "searchFilter": searchFilter,
        "searchVal":searchValue
    }
    let rp = await axios.post("/searchCV",ro);
    let rslist = rp.data.res;
    $("#search_result").text("");
    rslist.forEach(function(item){
       let source = item._source;
       let fullname = source.full_name != undefined ? source.full_name : "";
       let birthdate = source.birth_date != undefined ? source.birth_date : "";
       let address = source.address != undefined ? source.address : "";
       let phone = source.phone != undefined ? source.phone : "";
       let gender = source.gender != undefined ? source.gender : "";
       let major = source.major != undefined ? source.major : "";
       let cvContent = source.cv_content;
       let teamplate = `
       
       <div class="" data-ng-app="" data-ng-controller="myCtrl">
       <table>
         <tr>
           <th>Full name</th>
           <th>Birthdate</th>
           <th>Address</th>
           <th>Phone</th>
           <th>Gender</th>
           <th>Major</th>
           <th>CV Content</th>
         </tr>
         <tr data-ng-repeat="customer in people | filter: table">
           <td>${fullname}</td>
           <td>${birthdate}</td>
           <td>${address}</td>
           <td>${phone}</td>
           <td>${gender}</td>
           <td>${major}</td>
           <td>
             ${cvContent}
           </td>
         </tr>
       </table>
     </div>
       `;

       $("#search_result").append(teamplate);
    });

    $('html, body').animate({scrollTop:$(document).height()/3.5 - 20}, 'slow');
}