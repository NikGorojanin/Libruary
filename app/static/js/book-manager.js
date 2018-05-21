$(document).ready(function () {
    load_books_in_table();
    load_authors();
});

var load_books_in_table = function () {
    //$("#books-list").find("option").remove();
    $.ajax({
        type: "POST",
        url: "/load_books",
        success: function (data) {
            books_list = jQuery.parseJSON(data);
            if(books_list['status'] == "success")
            {
                $("#book_list_table").empty();
                if(books_list['data'].length > 0) {

                    table_content = "<tr class=\"header\">\n" +
                        "                <th style=\"width:100%;\">Книги</th>\n" +
                        "              </tr>";
                    $.each(books_list['data'], function (key, book) {
                        table_content += "<tr><td id=" + book['id'] + ">" + book['name'] + "</td></tr>"
                    });
                    $("#book_list_table").prepend(table_content);
                }
            }
            else
            {
                alert("Error: "+books_list['reason']);
            }
        }
    });
}


var load_authors = function () {
    $.ajax({
        type: "POST",
        url: "/load_authors",
        success: function (data) {
            authors_list = jQuery.parseJSON(data);
            if(authors_list['status'] == 'success')
            {
                $.each(authors_list['data'], function (key, author) {
                    $opt = $("<option />", { value: author['id'], text: author['name']});
                    $("#authors-list").append($opt);
                });
                $("#authors-list").multipleSelect("refresh");
            }
            else
            {
                alert("Error: "+authors_list['reason']);
            }
        }
    });
}


$('#add-book-btn').on('click', function () {
   book_name = $('.book-name').val();
   authors_ids = $('#authors-list').multipleSelect("getSelects");
   if(book_name.length > 0) {
       $.ajax({
           type: "POST",
           url: "/add_book",
           data: {
               'book_name': book_name,
               'authors_ids': JSON.stringify(authors_ids)
           },
           success: function (data) {
               add_result = jQuery.parseJSON(data);
               if (add_result['status'] != 'success') {
                   alert("Error: " + add_result['reason']);
               }
               else
               {
                   load_books_in_table();
                   alert("Книга добавлена");
               }
           }
       });
   }
   else
   {
       alert("Введите название книги");
   }
});

$("#book_list_table").on('click', 'td', function () {
    $('td').removeClass('focus');
    $(this).addClass('focus');

    book_id = $(this).attr("id");
    $.ajax({
           type: "POST",
           url: "/get_book",
           data: {
               'book_id': book_id,
           },
           success: function (data) {
                book_info = jQuery.parseJSON(data);
                if (book_info['status'] == 'success')
                {
                    $(".book-name").val(book_info['data']['book_name']);
                    $("#authors-list").multipleSelect("setSelects", book_info['data']['authors']);
                }
           }
    });
});

$("#save-book-btn").on('click', function(){
    book_id = $(".focus").attr('id');
    book_name = $('.book-name').val();
    authors_ids = $('#authors-list').multipleSelect("getSelects");
    $.ajax({type: "POST",
           url: "/save_book",
           data: {
               'book_id': book_id,
               'book_name': book_name,
               'authors_ids': JSON.stringify(authors_ids)
           },
           success: function (data) {
               save_result = jQuery.parseJSON(data);
               if (save_result['status'] != 'success') {
                   alert("Error: " + save_result['reason']);
               }
               else
               {
                   load_books_in_table();
                   alert("Книга сохранена");
               }
           }
    });
});

$("#remove-book-btn").on('click', function(){
    book_id = $(".focus").attr('id');
    // book_name = $('.book-name').val();
    // authors_ids = $('#authors-list').multipleSelect("getSelects");
    $.ajax({type: "POST",
           url: "/remove_book",
           data: {
               'book_id': book_id
           },
           success: function (data) {
               remove_result = jQuery.parseJSON(data);
               if (remove_result['status'] != 'success') {
                   alert("Error: " + remove_result['reason']);
               }
               else
               {
                   load_books_in_table();
                   alert("Книга удалена");
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
