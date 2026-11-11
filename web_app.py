import streamlit as st
from rembg import remove, new_session
from PIL import Image
import io

# إعداد الصفحة القياسي والمستقر
st.set_page_config(page_title="SmartRemover Pro")

st.title("🖼️ أداة تفريغ وعزل صور المنتجات أونلاين")
st.write("ارفع صورة منتجك ليقوم الذكاء الاصطناعي بتفريغها بدقة عالية فوراً وبدون تعليق.")

# تحميل النموذج أونلاين بأمان وثبات
@st.cache_resource
def load_session():
    return new_session("isnet-general-use")

try:
    session = load_session()
except Exception as e:
    st.error("جاري تجهيز سيرفر الذكاء الاصطناعي... يرجى تحديث الصفحة خلال لحظات.")

# أداة الرفع
uploaded_file = st.file_uploader("اختر صورة المنتج (PNG, JPG, JPEG, WEBP)...", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file is not None:
    input_image = Image.open(uploaded_file)
    st.image(input_image, caption="الصورة الأصلية المرفوعة", use_container_width=True)
    
    # 🎛️ أدوات التحكم المتقدمة لحل مشكلة بقايا الخلفية عند الحواف
    st.markdown("### ⚙️ إعدادات تنظيف الحواف المتقدمة")
    
    threshold = st.slider("1️⃣ قوة مسح الحواف والظلال الخلفية (Threshold):", min_value=5, max_value=240, value=60, step=5)
    
    erode_size = st.slider("2️⃣ حجم الممحاة الذكية لتآكل الحواف المتبقية (Erode Size):", min_value=0, max_value=30, value=10, step=2)
    
    if st.button("احذف الخلفية الآن وتنظيف الحواف", type="primary", use_container_width=True):
        with st.spinner("جاري تنظيف وتصفية الطبقات بدقة فائقة..."):
            try:
                # المعالجة المتقدمة باستخدام خيارات التآكل والتنظيف الديناميكي
                result_image = remove(
                    input_image,
                    session=session,
                    alpha_matting=True,
                    alpha_matting_foreground_threshold=240,
                    alpha_matting_background_threshold=threshold, # يتفاعل مع السلايدر الأول لالتهام البقايا
                    alpha_matting_erode_size=erode_size          # يتفاعل مع السلايدر الثاني لقص الحدود الزائدة عن الحواف
                )
                
                st.image(result_image, caption="النتيجة الشفافة والمفرغة بنجاح", use_container_width=True)
                
                buf = io.BytesIO()
                result_image.save(buf, format="PNG")
                byte_im = buf.getvalue()
                
                st.download_button(
                    label="📥 تحميل الصورة الشفافة بجودة عالية للرفع على سلة",
                    data=byte_im,
                    file_name="transparent_product_js.png",
                    mime="image/png",
                    use_container_width=True
                )
            except Exception as e:
                st.error("حدث خطأ أثناء معالجة الصورة في الخادم.")

st.markdown("<hr><p style='text-align: center; font-family: Consolas; color: #94a3b8; font-style: italic;'>Designed by: OSMAN ABBAS 2027</p>", unsafe_allow_html=True)
