import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

customers_df = pd.read_csv('customers_dataset.csv')
order_items_df = pd.read_csv('order_items_dataset.csv')
order_payments_df = pd.read_csv('order_payments_dataset.csv')
order_reviews_df = pd.read_csv('order_reviews_dataset.csv')
orders_df = pd.read_csv('orders_dataset.csv')
product_category_name_translation_df = pd.read_csv('product_category_name_translation.csv')
products_df = pd.read_csv('products_dataset.csv')
sellers_df = pd.read_csv('sellers_dataset.csv')

customers_df['customer_zip_code_prefix'].fillna(customers_df['customer_zip_code_prefix'].median(), inplace=True)

products_df.dropna(subset=['product_category_name'], inplace=True)

products_df['product_weight_g'].fillna(products_df['product_weight_g'].mean(), inplace=True)
products_df['product_length_cm'].fillna(products_df['product_length_cm'].mean(), inplace=True)
products_df['product_height_cm'].fillna(products_df['product_height_cm'].mean(), inplace=True)
products_df['product_width_cm'].fillna(products_df['product_width_cm'].mean(), inplace=True)

order_reviews_df['review_comment_title'].fillna('Tidak Ada Komentar', inplace=True)
order_reviews_df['review_comment_message'].fillna('Tidak Ada Komentar', inplace=True)

st.title("Analisis Data E-Commerce")

st.sidebar.title("Navigasi")
page = st.sidebar.radio("Pilih Halaman", ["Visualisasi", "Analisis RFM", "Kesimpulan"])

if page == "Visualisasi":
    st.header("Visualisasi")
    # Pertanyaan 1
    st.header("1. Produk apa saja yang paling sering dibeli oleh pelanggan?")

    product_orders = pd.merge(order_items_df, products_df, on='product_id', how='inner')
    product_counts = product_orders.groupby('product_id')['order_id'].count().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=product_counts[:10].index, y=product_counts[:10].values, ax=ax)
    plt.xlabel('ID Produk')
    plt.ylabel('Jumlah Pembelian')
    plt.title('10 Produk Paling Sering Dibeli')
    plt.xticks(rotation=90)
    st.pyplot(fig)

    st.subheader('Insight 1')
    st.write('Dari visualisasi di atas, kita bisa melihat 10 ID produk yang paling banyak dibeli. Kita bisa menindaklanjuti dengan melihat informasi produk lebih detail (misalnya nama produk, kategori) untuk memahami alasan produk tersebut banyak diminati.')


    # Pertanyaan 2
    st.header("2. Berapa rata-rata nilai transaksi yang dilakukan oleh pelanggan?")

    order_with_payment = pd.merge(orders_df, order_payments_df, on='order_id', how='inner')
    order_total_payment = order_with_payment.groupby('order_id')['payment_value'].sum()
    upper_limit = np.percentile(order_total_payment, 95)
    capped_order_total_payment = np.clip(order_total_payment, None, upper_limit)
    average_transaction_value = capped_order_total_payment.mean()

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(capped_order_total_payment, kde=True, ax=ax)
    plt.xlabel('Nilai Transaksi')
    plt.ylabel('Frekuensi')
    plt.title('Distribusi Nilai Transaksi (Dengan Capping)')
    plt.axvline(average_transaction_value, color='red', linestyle='dashed', linewidth=2, label='Rata-rata Nilai Transaksi')
    plt.legend()
    st.pyplot(fig)
    st.write(f"Rata-rata Nilai Transaksi: {average_transaction_value:.2f}")

    st.subheader('Insight 2')
    st.write('Berdasarkan histogram yang dihasilkan, kita dapat melihat bahwa:') 
    st.write('1. Sebagian besar transaksi memiliki nilai yang relatif rendah. ')
    st.write('2. Distribusi nilai transaksi cenderung condong ke kanan (right-skewed), artinya ada beberapa transaksi dengan nilai yang sangat tinggi yang memengaruhi rata-rata. ')
    st.write('3. Untuk mengurangi pengaruh outlier, capping pada nilai transaksi dilakukan dengan membatasi nilai transaksi pada persentil ke-95.')
    st.write('4. Rata-rata nilai transaksi setelah capping menunjukkan nilai transaksi rata-rata yang lebih representatif dan tidak dipengaruhi oleh nilai outlier.')
    st.write('5. Garis merah putus-putus menunjukkan rata-rata nilai transaksi yang telah dihitung setelah proses capping. ')
    st.write('Dengan demikian, analisis ini memberikan informasi yang lebih akurat mengenai nilai transaksi rata-rata pelanggan, dengan mempertimbangkan faktor outlier yang dapat mempengaruhi hasil analisis.')

    # Pertanyaan 3
    st.header("3. Di kota mana pelanggan paling banyak melakukan pembelian?")

    customer_orders = pd.merge(customers_df, orders_df, on='customer_id', how='inner')
    city_order_counts = customer_orders.groupby('customer_city')['order_id'].count().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=city_order_counts[:10].index, y=city_order_counts[:10].values, ax=ax)
    plt.xlabel('Kota')
    plt.ylabel('Jumlah Pembelian')
    plt.title('10 Kota dengan Jumlah Pembelian Terbanyak')
    plt.xticks(rotation=90)
    st.pyplot(fig)

    st.subheader('Insight 3')
    st.write('- Visualisasi ini menunjukkan 10 kota dengan jumlah pembelian terbanyak.')
    st.write('- Informasi ini dapat membantu dalam menentukan strategi pemasaran yang lebih tertarget.')
    st.write('- Misalnya, kita dapat fokus pada promosi di kota-kota dengan jumlah pembelian yang tinggi untuk meningkatkan penjualan dan jangkauan pasar.')
    st.write('- Kita juga dapat menganalisis lebih lanjut faktor-faktor yang berkontribusi pada jumlah pembelian di kota-kota tersebut, seperti daya beli, demografi, dan preferensi pelanggan.')


    # Pertanyaan 4
    st.header("4. Kategori produk apa yang paling menguntungkan bagi bisnis?")

    product_orders_with_price = pd.merge(order_items_df, products_df, on='product_id', how='inner')
    product_orders_with_price = pd.merge(product_orders_with_price, product_category_name_translation_df, on='product_category_name', how='left')

    category_revenue = product_orders_with_price.groupby('product_category_name_english')['price'].sum().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=category_revenue[:10].index, y=category_revenue[:10].values, ax=ax)
    plt.xlabel('Kategori Produk')
    plt.ylabel('Total Pendapatan')
    plt.title('10 Kategori Produk dengan Pendapatan Tertinggi')
    plt.xticks(rotation=90)
    st.pyplot(fig)

    st.subheader('Insight 4')
    st.write('- Visualisasi ini menunjukkan 10 kategori produk dengan total pendapatan tertinggi.')
    st.write('- Informasi ini dapat menjadi dasar dalam pengambilan keputusan terkait pengembangan produk atau penawaran promosi.')
    st.write('- Misalnya, bisnis dapat fokus pada pengembangan produk di kategori yang paling menguntungkan untuk meningkatkan pendapatan.')
    st.write('- Kita juga dapat menganalisis lebih lanjut faktor-faktor yang berkontribusi pada keuntungan kategori tersebut, seperti margin keuntungan, volume penjualan, dan tingkat kepuasan pelanggan.')
    st.write('- Selain itu, kita juga dapat menganalisis hubungan antara kategori produk dan tren pembelian. Misalnya, apakah kategori produk tertentu mengalami peningkatan penjualan dalam beberapa bulan terakhir.')


    # Pertanyaan 5
    st.header("5. Bagaimana distribusi rating review pelanggan terhadap produk yang dibeli?")

    order_review_with_product = pd.merge(order_reviews_df, order_items_df, on='order_id', how='inner')

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(x='review_score', data=order_review_with_product, ax=ax)
    plt.xlabel('Rating Review')
    plt.ylabel('Jumlah Review')
    plt.title('Distribusi Rating Review Pelanggan')
    st.pyplot(fig)

    st.subheader('Insight 5')
    st.write('- Visualisasi ini menunjukkan bagaimana distribusi rating review pelanggan terhadap produk yang dibeli.')
    st.write('- Kita bisa melihat berapa banyak pelanggan yang memberikan rating 1, 2, 3, 4, dan 5.')
    st.write('- Jika terdapat banyak review dengan rating rendah (1-3), maka perlu dilakukan analisis lebih lanjut untuk mengetahui penyebabnya, seperti kualitas produk, layanan pelanggan, atau masalah pengiriman.')
    st.write('- Informasi ini dapat membantu bisnis untuk meningkatkan kualitas produk dan layanan agar dapat meningkatkan kepuasan pelanggan.')

elif page == "Analisis RFM":
    st.header("Analisis RFM (Recency, Frequency, Monetary)")
    # Fungsi untuk menampilkan visualisasi di Streamlit
    def plot_countplot(data, column, title, xlabel, ylabel):
        plt.figure(figsize=(12, 6))
        sns.countplot(x=column, data=data)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        st.pyplot(plt.gcf())

    # Menggabungkan data dan menghitung Recency, Frequency, dan Monetary
    rfm_data = pd.merge(orders_df, order_payments_df, on='order_id', how='inner')
    rfm_data = pd.merge(rfm_data, customers_df, on='customer_id', how='inner')

    rfm_data['order_purchase_timestamp'] = pd.to_datetime(rfm_data['order_purchase_timestamp'])

    last_date = rfm_data['order_purchase_timestamp'].max()

    rfm_table = rfm_data.groupby('customer_id').agg({
        'order_purchase_timestamp': lambda x: (last_date - x.max()).days,  # Recency
        'order_id': 'count',  # Frequency
        'payment_value': 'sum'  # Monetary
    })

    rfm_table.rename(columns={
        'order_purchase_timestamp': 'Recency',
        'order_id': 'Frequency',
        'payment_value': 'Monetary'
    }, inplace=True)

    quantiles = rfm_table.quantile(q=[0.25, 0.5, 0.75])

    segments = {
        'Recency': {
            'High': lambda x: x <= quantiles['Recency'][0.25],
            'Medium': lambda x: quantiles['Recency'][0.25] < x <= quantiles['Recency'][0.75],
            'Low': lambda x: x > quantiles['Recency'][0.75]
        },
        'Frequency': {
            'High': lambda x: x >= quantiles['Frequency'][0.75],
            'Medium': lambda x: quantiles['Frequency'][0.25] <= x < quantiles['Frequency'][0.75],
            'Low': lambda x: x < quantiles['Frequency'][0.25]
        },
        'Monetary': {
            'High': lambda x: x >= quantiles['Monetary'][0.75],
            'Medium': lambda x: quantiles['Monetary'][0.25] <= x < quantiles['Monetary'][0.75],
            'Low': lambda x: x < quantiles['Monetary'][0.25]
        }
    }

    def assign_segment(row):
        recency_segment = 'Low'
        for segment, condition in segments['Recency'].items():
            if condition(row['Recency']):
                recency_segment = segment
                break

        frequency_segment = 'Low'
        for segment, condition in segments['Frequency'].items():
            if condition(row['Frequency']):
                frequency_segment = segment
                break

        monetary_segment = 'Low'
        for segment, condition in segments['Monetary'].items():
            if condition(row['Monetary']): 
                monetary_segment = segment
                break

        return recency_segment, frequency_segment, monetary_segment

    rfm_table[['Recency_Segment', 'Frequency_Segment', 'Monetary_Segment']] = rfm_table.apply(assign_segment, axis=1, result_type='expand')

    # Judul di Streamlit
    st.title('RFM Segmentation Analysis')

    # Visualisasi Segmen Pelanggan Berdasarkan Recency
    st.subheader('Segmen Pelanggan Berdasarkan Recency')
    plot_countplot(rfm_table, 'Recency_Segment', 'Segmen Pelanggan Berdasarkan Recency', 'Recency Segment', 'Jumlah Pelanggan')

    # Visualisasi Segmen Pelanggan Berdasarkan Frequency
    st.subheader('Segmen Pelanggan Berdasarkan Frequency')
    plot_countplot(rfm_table, 'Frequency_Segment', 'Segmen Pelanggan Berdasarkan Frequency', 'Frequency Segment', 'Jumlah Pelanggan')

    # Visualisasi Segmen Pelanggan Berdasarkan Monetary
    st.subheader('Segmen Pelanggan Berdasarkan Monetary')
    plot_countplot(rfm_table, 'Monetary_Segment', 'Segmen Pelanggan Berdasarkan Monetary', 'Monetary Segment', 'Jumlah Pelanggan')

    st.subheader('Insight RFM Analysis')
    st.write('- Pelanggan dengan skor Recency tinggi (High) dan Frequency tinggi (High) adalah pelanggan terbaik yang loyal dan sering berbelanja.')
    st.write('- Pelanggan dengan skor Recency rendah (Low) dan Frequency rendah (Low) adalah pelanggan yang sudah lama tidak berbelanja dan jarang berbelanja, perlu diberikan perhatian khusus.')
    st.write('- Pelanggan dengan skor Monetary tinggi (High) adalah pelanggan yang memberikan pendapatan terbesar, perlu diberikan program loyalitas dan retensi.')
    st.write('- Pelanggan dengan skor Monetary rendah (Low) adalah pelanggan yang memberikan pendapatan kecil, perlu ditingkatkan dengan promosi atau penawaran khusus.')

elif page == "Kesimpulan":
    st.header("Kesimpulan & Rekomendasi")
    st.write('Berdasarkan analisis yang telah dilakukan, ada beberapa poin penting terkait perilaku pelanggan, tren penjualan, dan aspek bisnis yang dapat dijadikan dasar pengambilan keputusan strategis.')

    st.subheader('1. Produk Populer:')
    st.write('Produk-produk dengan penjualan tertinggi menunjukkan bahwa mereka memiliki daya tarik yang besar di mata pelanggan. Dengan menganalisis lebih lanjut tentang nama, kategori, dan fitur dari produk-produk tersebut, perusahaan dapat memahami lebih dalam tentang preferensi konsumen, sehingga dapat menyesuaikan strategi produksi dan pemasaran.')
    st.subheader('2. Nilai Transaksi:')
    st.write('Rata-rata nilai transaksi mencerminkan kemampuan beli pelanggan. Segmen pelanggan dapat dikelompokkan berdasarkan daya beli mereka, dan ini bisa dijadikan dasar untuk merancang strategi harga yang lebih personal atau promosi yang lebih sesuai untuk tiap kelompok.')
    st.subheader('3. Lokasi Pelanggan:')
    st.write('Beberapa wilayah menunjukkan volume transaksi yang tinggi. Wilayah-wilayah ini bisa menjadi fokus utama dalam strategi pemasaran, sehingga kampanye bisa lebih tepat sasaran dan lebih efisien.')
    st.subheader('4. Kategori Produk Menguntungkan:')
    st.write('Terdapat kategori produk tertentu yang memberikan kontribusi besar terhadap pendapatan perusahaan. Fokus pada kategori ini, baik melalui inovasi produk maupun promosi, dapat mendorong peningkatan pendapatan lebih lanjut.')
    st.subheader('5. Kepuasan Pelanggan:')
    st.write('Rating produk dari pelanggan memberikan gambaran tentang tingkat kepuasan mereka. Penilaian yang buruk bisa jadi disebabkan oleh kualitas produk, pelayanan, atau masalah pengiriman. Mengatasi masalah-masalah ini dapat meningkatkan kepuasan dan loyalitas pelanggan.')
    st.subheader('6. Analisis RFM (Recency, Frequency, Monetary):')
    st.write('Dengan menggunakan analisis RFM, perusahaan dapat mengelompokkan pelanggan berdasarkan kapan mereka terakhir membeli, seberapa sering mereka membeli, dan berapa banyak mereka menghabiskan uang. Pelanggan yang sering berbelanja dan memiliki transaksi tinggi harus menjadi prioritas dalam program loyalitas. Sementara itu, pelanggan yang jarang berbelanja perlu diaktifkan kembali dengan kampanye khusus.')
    st.subheader('Rekomendasi Strategis:')
    st.write('Pengembangan Produk: Fokus pada produk yang berada di kategori terlaris dan paling menguntungkan untuk meningkatkan pendapatan secara keseluruhan.')
    st.write('Strategi Pemasaran: Optimalkan pemasaran dengan menargetkan wilayah dengan volume pembelian tinggi. Selain itu, program promosi bisa diarahkan pada segmen pelanggan tertentu, seperti yang teridentifikasi dalam analisis RFM.')
    st.write('Peningkatan Layanan: Tangani masalah yang mengakibatkan penilaian negatif dari pelanggan, baik itu terkait kualitas produk, pengiriman, atau layanan pelanggan, guna meningkatkan kepuasan pelanggan.')
    st.write('Program Loyalitas: Rancang program loyalitas yang dirancang untuk mempertahankan pelanggan yang sering berbelanja dan bertransaksi dalam jumlah besar.')
    st.write('Analisis Lanjutan: Lakukan analisis lebih dalam terkait tren belanja dan perilaku pelanggan untuk menemukan peluang bisnis baru dan memperbaiki aspek-aspek yang belum optimal.')
    st.subheader('Kesimpulan Akhir:')
    st.write('Analisis ini memberikan gambaran jelas tentang tren dan pola yang terjadi dalam bisnis e-commerce. Jika perusahaan dapat mengambil langkah-langkah berdasarkan insight yang ditemukan, maka potensi untuk meningkatkan keuntungan, efisiensi, dan pengalaman pelanggan dapat terwujud. Namun, analisis lanjutan diperlukan untuk menyempurnakan strategi bisnis, terutama dengan mempertimbangkan faktor eksternal seperti kompetisi dan dinamika pasar.')