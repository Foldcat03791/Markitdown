import streamlit as st
import os
from markitdown import MarkItDown
from io import StringIO

# 设置页面配置
st.set_page_config(
    page_title="MarkItDown - 文件转换器",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初始化 MarkItDown
@st.cache_resource
def get_markitdown():
    return MarkItDown()

md = get_markitdown()

# 侧边栏
st.sidebar.title("📝 MarkItDown")
st.sidebar.markdown("---")
st.sidebar.markdown("""
### 支持的文件格式：
- 📄 PDF
- 📝 Word (.docx)
- 📊 Excel (.xlsx, .xls)
- 📽️ PowerPoint (.pptx)
- 🌐 HTML
- 📋 CSV, JSON, XML
- 📦 ZIP
- 📚 EPUB
- 🖼️ 图片
- 🎵 音频
- 📧 Outlook
- 📓 Jupyter Notebook
""")

st.sidebar.markdown("---")
st.sidebar.info("💡 拖放文件到主区域开始转换")

# 主界面
st.title("📝 MarkItDown 文件转换器")
st.markdown("将各种文件格式转换为 Markdown，方便与 LLM 配合使用")
st.markdown("---")

# 文件上传区域
uploaded_file = st.file_uploader(
    "选择要转换的文件",
    type=["pdf", "docx", "xlsx", "xls", "pptx", "html", "csv", "json", "xml", "zip", "epub", "jpg", "jpeg", "png", "mp3", "wav", "msg", "ipynb"],
    help="支持多种文件格式，一次上传一个文件"
)

if uploaded_file is not None:
    # 显示文件信息
    file_details = {
        "文件名": uploaded_file.name,
        "文件类型": uploaded_file.type,
        "文件大小": f"{uploaded_file.size / 1024:.2f} KB"
    }
    
    col1, col2, col3 = st.columns(3)
    col1.metric("📁 文件名", uploaded_file.name)
    col2.metric("📎 类型", uploaded_file.type.split('/')[-1].upper())
    col3.metric("📏 大小", f"{uploaded_file.size / 1024:.2f} KB")
    
    st.markdown("---")
    
    # 转换按钮
    if st.button("🚀 开始转换", type="primary", use_container_width=True):
        with st.spinner("正在转换文件..."):
            try:
                # 保存临时文件
                temp_file = f"temp_{uploaded_file.name}"
                with open(temp_file, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # 执行转换
                result = md.convert(temp_file)
                
                # 删除临时文件
                os.remove(temp_file)
                
                # 显示结果
                st.success("✅ 转换成功！")
                st.markdown("---")
                
                # 结果显示区域
                st.subheader("📄 转换结果")
                
                # 创建两个标签页：预览和下载
                tab1, tab2 = st.tabs(["👁️ 预览", "💾 下载"])
                
                with tab1:
                    # 显示 Markdown 预览
                    st.markdown(result.text_content)
                
                with tab2:
                    # 下载按钮
                    output_filename = os.path.splitext(uploaded_file.name)[0] + ".md"
                    st.download_button(
                        label="📥 下载 Markdown 文件",
                        data=result.text_content,
                        file_name=output_filename,
                        mime="text/markdown",
                        use_container_width=True
                    )
                    
                    # 显示原始内容
                    st.text_area("原始内容", result.text_content, height=400)
                
            except Exception as e:
                st.error(f"❌ 转换失败: {str(e)}")
                st.info("请尝试其他文件或检查文件是否损坏")

else:
    # 空状态提示
    st.info("👆 请在上方上传文件开始转换")
    
    # 显示示例
    with st.expander("📖 查看使用示例"):
        st.markdown("""
        ### 示例 1：转换 PDF 文档
        ```
        上传 report.pdf → 得到 report.md
        ```
        
        ### 示例 2：转换 Excel 表格
        ```
        上传 data.xlsx → 表格转换为 Markdown 格式
        ```
        
        ### 示例 3：转换网页
        ```
        上传 page.html → 提取主要内容为 Markdown
        ```
        """)

# 页脚
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>Made with ❤️ using MarkItDown</p>
    </div>
    """,
    unsafe_allow_html=True
)
