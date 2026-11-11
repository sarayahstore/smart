import streamlit as st
from rembg import remove, new_session
from PIL import Image
import io

# إعداد الصفحة القياسي والمستقر لمنع مشكلة الشاشة البيضاء
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
    
    threshold = st.slider("🎛️ قوة مسح الحواف والظلال الخلفية:", min_value=5, max_value=240, value=40, step=5)
    
    if st.button("احذف الخلفية الآن", type="primary", use_container_width=True):
        with st.spinner("جاري تنظيف وتصفية الطبقات بدقة..."):
            try:
                result_image = remove(
                    input_image,
                    session=session,
                    alpha_matting=True,
                    alpha_matting_foreground_threshold=240,
                    alpha_matting_background_threshold=threshold,
                    alpha_matting_erode_size=10
                )
                
                st.image(result_image, caption="النتيجة الشفافة والمفرغة", use_container_width=True)
                
                buf = io.BytesIO()
                result_image.save(buf, format="PNG")
                byte_im = buf.getvalue()
                
                st.download_button(
                    label="📥 تحميل الصورة الشفافة بجودة عالية (PNG)",
                    data=byte_im,
                    file_name="transparent_product.png",
                    mime="image/png",
                    use_container_width=True
                )
            except Exception as e:
                st.error("حدث خطأ أثناء معالجة الصورة في الخادم.")

st.markdown("<hr><p style='text-align: center; font-family: Consolas; color: #94a3b8; font-style: italic;'>Designed by: OSMAN ABBAS</p>", unsafe_allow_html=True)
