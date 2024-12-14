$(document).ready(function() {
    let editExpenseId = null;
    let deleteExpenseId = null;

    // Fungsi untuk menampilkan data pengeluaran
    function loadExpenses() {
        $.get('/get_expenses', function(data) {
            $('#expense-table-body').empty();  // Kosongkan tabel sebelum mengisi ulang

            let totalAmount = 0;
            data.expenses.forEach(function(expense) {
                totalAmount += expense.amount;
                const row = `
                    <tr data-id="${expense.id}">
                        <td>${expense.category}</td>
                        <td>${expense.amount}</td>
                        <td>${expense.date}</td>
                        <td><button class="edit-btn">Edit</button></td>
                        <td><button class="delete-btn">Delete</button></td>
                    </tr>
                `;
                $('#expense-table-body').append(row);
            });

            // Menampilkan total amount
            $('#total-amount').text(totalAmount);
        });
    }

    // Fungsi untuk menampilkan modal Edit
    $(document).on('click', '.edit-btn', function() {
        const row = $(this).closest('tr');
        editExpenseId = row.data('id');
        const category = row.find('td:nth-child(1)').text();
        const amount = row.find('td:nth-child(2)').text();
        const date = row.find('td:nth-child(3)').text();

        $('#edit-category').val(category);
        $('#edit-amount').val(amount);
        $('#edit-date').val(date);

        $('#editModal').show();  // Tampilkan modal edit
    });

    // Menyimpan perubahan edit pengeluaran
    $('#save-edit-btn').on('click', function() {
        const category = $('#edit-category').val();
        const amount = $('#edit-amount').val();
        const date = $('#edit-date').val();

        $.ajax({
            url: '/edit_expense/' + editExpenseId,
            method: 'PUT',
            data: {
                category: category,
                amount: amount,
                date: date
            },
            success: function(response) {
                $('#editModal').hide();  // Sembunyikan modal setelah edit
                loadExpenses();  // Refresh daftar pengeluaran
            }
        });
    });

    // Menutup modal edit
    $('#close-edit-btn').on('click', function() {
        $('#editModal').hide();
    });

    // Fungsi untuk menampilkan modal Delete
    $(document).on('click', '.delete-btn', function() {
        const row = $(this).closest('tr');
        deleteExpenseId = row.data('id');

        $('#deleteModal').show();  // Tampilkan modal delete
    });

    // Menghapus pengeluaran
    $('#confirm-delete-btn').on('click', function() {
        $.ajax({
            url: '/delete_expense/' + deleteExpenseId,
            method: 'DELETE',
            success: function(response) {
                $('#deleteModal').hide();  // Sembunyikan modal setelah delete
                loadExpenses();  // Refresh daftar pengeluaran
            }
        });
    });

    // Menutup modal delete
    $('#close-delete-btn').on('click', function() {
        $('#deleteModal').hide();
    });

    // Menambahkan pengeluaran baru
    $('#add-btn').on('click', function() {
        const category = $('#category-select').val();
        const amount = $('#amount-input').val();
        const date = $('#date-input').val();

        $.post('/add_expense', {
            category: category,
            amount: amount,
            date: date
        }, function(response) {
            loadExpenses();  // Refresh daftar pengeluaran
        });
    });

    // Menampilkan pengeluaran saat pertama kali dimuat
    loadExpenses();
});
