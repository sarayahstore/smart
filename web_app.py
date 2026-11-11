import streamlit as st
from rembg import remove, new_session
from PIL import Image
import io

# إعداد الصفحة وتفعيل الوضع الفاتح الافتراضي للمتصفحات
st.set_page_config(page_title="SmartRemover Pro", layout="centered", initial_sidebar_state="collapsed")

# تصميم ترويسة الصفحة بالوضع الفاتح
st.markdown("<h2 style='text-align: center; color: #1d4ed8;'>🖼️ أداة تفريغ وعزل صور المنتجات أونلاين</h2>", unsafe_allow_width=True)
st.markdown("<p style='text-align: center; color: #475569;'>ارفع صورة منتجك ليقوم الذكاء الاصطناعي بتفريغها بدقة عالية فوراً</p>", unsafe_allow_width=True)

# تفعيل الجلسة مع أفضل نموذج عزل احترافي للمنتجات المعقدة
@st.cache_resource
def load_session():
    return new_session("isnet-general-use")

session = load_session()

# أداة رفع ملفات الصور للموقع أونلاين
uploaded_file = st.file_uploader("اختر صورة المنتج المعقدة (PNG, JPG, JPEG, WEBP)...", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file is not None:
    input_image = Image.open(uploaded_file)
    
    # عرض المعاينة للصورة الأصلية
    st.image(input_image, caption="الصورة الأصلية المرفوعة", use_container_width=True)
    
    # شريط التمرير (Slider) للتحكم في دقة الحواف والظلال أونلاين
    threshold = st.slider("🎛️ قوة مسح الحواف والظلال الخلفية:", min_value=5, max_value=240, value=40, step=5)
    
    if st.button("احذف الخلفية الآن وتأكد من الحواف", type="primary", use_container_width=True):
        with st.spinner("جاري تطبيق خوارزميات عزل الطبقات بدقة فائقة..."):
            try:
                # المعالجة والمسح بالذكاء الاصطناعي بناءً على قيمة السلايدر أونلاين
                result_image = remove(
                    input_image,
                    session=session,
                    alpha_matting=True,
                    alpha_matting_foreground_threshold=240,
                    alpha_matting_background_threshold=threshold,
                    alpha_matting_erode_size=10
                )
                
                # تحويل الصورة إلى بايتس لتجهيزها للتحميل المباشر للمستخدم
                buf = io.BytesIO()
                result_image.save(buf, format="PNG")
                byte_im = buf.getvalue()
                
                # عرض النتيجة الشفافة النهائية
                st.image(result_image, caption="النتيجة الشفافة والمفرغة بنجاح", use_container_width=True)
                
                # زر التحميل المباشر للمتصفح
                st.download_button(
                    label="📥 تحميل الصورة الشفافة بجودة عالية للرفع على سلة",
                    data=byte_im,
                    file_name="transparent_product_js.png",
                    mime="image/png",
                    use_container_width=True
                )
            except Exception as e:
                st.error("حدث خطأ أثناء معالجة الصورة، يرجى إعادة المحاولة.")

# حقوق المصمم دائم وثابت أسفل صفحة الويب
st.markdown("<hr><p style='text-align: center; font-family: Consolas; color: #94a3b8; font-style: italic;'>Designed by: OSMAN ABBAS 2027</p>", unsafe_allow_html=True)
