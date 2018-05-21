$(document).ready(function () {
    load_authors_in_table();
    load_books();
});

var load_authors_in_table = function () {
    //$("#books-list").find("option").remove();
    $.ajax({
        type: "POST",
        url: "/load_authors",
        success: function (data) {
            authors_list = jQuery.parseJSON(data);
            if(authors_list['status'] == "success")
            {
                $("#author_list_table").empty();
                if(authors_list['data'].length > 0) {

                    table_content = "<tr class=\"header\">\n" +
                        "                <th style=\"width:100%;\">Авторы</th>\n" +
                        "              </tr>";
                    $.each(authors_list['data'], function (key, author) {
                        table_content += "<tr><td id=" + author['id'] + ">" + author['name'] + "</td></tr>"
                    });
                    $("#author_list_table").prepend(table_content);
                }
            }
            else
            {
                alert("Error: "+authors_list['reason']);
            }
        }
    });
}


var load_books = function () {
    $.ajax({
        type: "POST",
        url: "/load_books",
        success: function (data) {
            books_list = jQuery.parseJSON(data);
            if(books_list['status'] == 'success')
            {
                $.each(books_list['data'], function (key, book) {
                    $opt = $("<option />", { value: book['id'], text: book['name']});
                    $("#books-list").append($opt);
                });
                $("#books-list").multipleSelect("refresh");
            }
            else
            {
                alert("Error: "+authors_list['reason']);
            }
        }
    });
}


$('#add-author-btn').on('click', function () {
   author_name = $('.author-name').val();
   books_ids = $('#books-list').multipleSelect("getSelects");
   if(author_name.length > 0) {
       $.ajax({
           type: "POST",
           url: "/add_author",
           data: {
               'author_name': author_name,
               'books_ids': JSON.stringify(books_ids)
           },
           success: function (data) {
               add_result = jQuery.parseJSON(data);
               if (add_result['status'] != 'success') {
                   alert("Error: " + add_result['reason']);
               }
               else
               {
                   load_authors_in_table();
                   alert("Автор добавлен");
               }
           }
       });
   }
   else
   {
       alert("Введите имя автора");
   }
});


$("#author_list_table").on('click', 'td', function () {
    $('td').removeClass('focus');
    $(this).addClass('focus');

    author_id = $(this).attr("id");
    $.ajax({
           type: "POST",
           url: "/get_author",
           data: {
               'author_id': author_id,
           },
           success: function (data) {
                author_info = jQuery.parseJSON(data);
                if (author_info['status'] == 'success')
                {
                    $(".author-name").val(author_info['data']['author_name']);
                    $("#books-list").multipleSelect("setSelects", author_info['data']['books']);
                }
           }
    });
});

$("#save-author-btn").on('click', function(){
    author_id = $(".focus").attr('id');
    author_name = $('.author-name').val();
    books_ids = $('#books-list').multipleSelect("getSelects");
    $.ajax({type: "POST",
           url: "/save_author",
           data: {
               'author_id': author_id,
               'author_name': author_name,
               'books_ids': JSON.stringify(books_ids)
           },
           success: function (data) {
               save_result = jQuery.parseJSON(data);
               if (save_result['status'] != 'success') {
                   alert("Error: " + save_result['reason']);
               }
               else
               {
                   load_authors_in_table();
                   alert("Автор сохранен");
               }
           }
    });
});


$("#remove-author-btn").on('click', function(){
    author_id = $(".focus").attr('id');
    alert(author_id);
    // book_name = $('.book-name').val();
    // authors_ids = $('#authors-list').multipleSelect("getSelects");
    $.ajax({type: "POST",
           url: "/remove_author",
           data: {
               'author_id': author_id
           },
           success: function (data) {
               remove_result = jQuery.parseJSON(data);
               if (remove_result['status'] != 'success') {
                   alert("Error: " + remove_result['reason']);
               }
               else
               {
                   load_authors_in_table();
                   alert("Автор удален");
               }
           }
    });
});


$("#myInput").on("keyup", function () {
    cur_text = $("#myInput").val().toLowerCase();
    lines = document.getElementsByTagName("tr");
    //console.log(lines);
    if (lines.length > 1) {
        for (i = 1; i < lines.length; i++) {
            book = lines[i].getElementsByTagName("td")[0];
            if (book.innerHTML.toLowerCase().indexOf(cur_text) > -1)
                lines[i].style.display = "";
            else
                lines[i].style.display = "none";
        }
    }
});