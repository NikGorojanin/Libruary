$(document).ready(function () {
    load_table_data();
});


var load_table_data = function () {
    $.ajax({
        type: "POST",
        url: "/load_table_data",
        success: function (data) {
            books_list = jQuery.parseJSON(data);
            if(books_list['status'] == "success")
            {
                $("#libruary_table").empty();
                table_content = "<tr class=\"header\">\n" +
                    "                <th style=\"width:60%;\">Книги</th>\n" +
                    "                <th style=\"width:40%;\">Авторы</th>\n" +
                    "              </tr>";
                $.each(books_list['data'], function (key, value) {
                    table_content += "<tr><td>"+value['book']+"</td><td>"+value['author']+"</td></tr>";
                });
                $("#libruary_table").prepend(table_content);
            }
            else
            {
                alert("Error: "+books_list['reason']);
            }
        }
    });
}

$("#myInput").on("keyup", function () {
    cur_text = $("#myInput").val().toLowerCase();
   lines = document.getElementsByTagName("tr");
    //console.log(lines);
    if (lines.length > 1)
    {
        for(i=1;i<lines.length;i++)
        {
            ceils = lines[i].getElementsByTagName("td");
            if (ceils.length == 2) {
                book = ceils[0];
                author = ceils[1];
                if (book.innerHTML.toLowerCase().indexOf(cur_text) > -1 || author.innerHTML.toLowerCase().indexOf(cur_text) > -1)
                    lines[i].style.display = "";
                else
                    lines[i].style.display = "none";
            }
        }
    }
   // lines = tbody.getElementsByTagName("tr");
   // console.log(lines.length);
   // for (i = 0; i<lines.length; i++)
   // {
   //     book_td = lines[i].getElementsByTagName("td")[0];
   //     author_td = lines[i].getElementsByTagName("td")[1];
   //     if (book_td && author_td)
   //     {
   //         console.log(book_td.innerHTML.toLowerCase());
   //         console.log(author_td.innerHTML.toLowerCase());
   //         if (book_td.innerHTML.toLowerCase().indexOf(cur_text) > -1 || author_td.innerHTML.toLowerCase().indexOf(cur_text) > -1)
   //             lines[i].style.display = "";
   //         else
   //             lines[i].style.display = "none";
   //     }
   // }
});
