import os 
import streamlit as st
import streamlit.components.v1 as components
from streamlit_custom_sidebar import IS_RELEASE

if not IS_RELEASE:
    _component_func = components.declare_component(
      
        "my_component",
        url="http://localhost:3001",
    )
else:

    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("my_component", path=build_dir)

def myComponent(initialPage="example", key="testing", default="example"):

    component_value = _component_func(initialPage=initialPage, key=key, default=default)

    return component_value


class SidebarIcons:

    def __init__(self, append_CDN_to=None) -> None:
        self.append_CDN_to = append_CDN_to
    
    def Load_All_CDNs(self):
        """
        Load all the CDNs for the supported icon libraries. These include:
        - Google-material-symbols
        - Remix icon
        - Tabler Icons
        - Icon-8
        - line-awesome
        """

        linkJS = """
            <script>
                exists = window.top.document.querySelectorAll('link[href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@48,400,0,0"]')
             
                if (exists.length === 0 ){{
                    const GoogleEmoji = document.createElement("link");
                    GoogleEmoji.href = "https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@48,400,0,0";
                    GoogleEmoji.rel = "stylesheet";
                    window.top.document.head.appendChild(GoogleEmoji);

                    const remixIcon = document.createElement("link");
                    remixIcon.href = "https://cdn.jsdelivr.net/npm/remixicon@3.5.0/fonts/remixicon.css";
                    remixIcon.rel = "stylesheet";
                    window.top.document.head.appendChild(remixIcon);

                    const tablerIcons = document.createElement("link");
                    tablerIcons.href = "https://cdn.jsdelivr.net/npm/@tabler/icons@latest/iconfont/tabler-icons.min.css";
                    tablerIcons.rel = "stylesheet";
                    window.top.document.head.appendChild(tablerIcons); 

                    const tablerIcons_2 = document.createElement("link");
                    tablerIcons_2.href ="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css";      
                    tablerIcons_2.rel = "stylesheet";
                    window.top.document.head.appendChild(tablerIcons_2);   

                    const tablerIcons_3 = document.createElement("script")
                    tablerIcons_3.src = "https://cdn.jsdelivr.net/npm/@tabler/icons@latest/icons-react/dist/index.umd.min.js"
                    window.top.document.head.appendChild(tablerIcons_3) 

                    removeJs = parent.document.querySelectorAll('iframe[srcdoc*="GoogleEmoji"]')[0].parentNode
                    removeJs.style = 'display:none;'
                }} else {{
                    
                    removeJs = parent.document.querySelectorAll('iframe[srcdoc*="GoogleEmoji"]')[0].parentNode
                    removeJs.style = 'display:none;'
                }}

            </script>
        """
        st.components.v1.html(linkJS, height=0, width=0)

    def Load_All_CDNs_to_streamlit_cloud(self):
        query = "iframe[title='streamlitApp']"

        linkJS = f"""
            <script>
                headToAppendIframe = window.top.document.querySelectorAll("{query}")[0].contentDocument.head

                exists = window.top.document.querySelectorAll('link[href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@48,400,0,0"]')

                if (exists.length === 0){{
                    const GoogleEmoji = document.createElement("link");
                    GoogleEmoji.href = "https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@48,400,0,0";
                    GoogleEmoji.rel = "stylesheet";
                    headToAppendIframe.appendChild(GoogleEmoji);

                    const remixIcon = document.createElement("link");
                    remixIcon.href = "https://cdn.jsdelivr.net/npm/remixicon@3.5.0/fonts/remixicon.css";
                    remixIcon.rel = "stylesheet";
                    headToAppendIframe.appendChild(remixIcon);

                    const tablerIcons = document.createElement("link");
                    tablerIcons.href = "https://cdn.jsdelivr.net/npm/@tabler/icons@latest/iconfont/tabler-icons.min.css";
                    tablerIcons.rel = "stylesheet";
                    headToAppendIframe.appendChild(tablerIcons); 

                    const tablerIcons_2 = document.createElement("link");
                    tablerIcons_2.href ="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css";      
                    tablerIcons_2.rel = "stylesheet";
                    headToAppendIframe.appendChild(tablerIcons_2);   

                    const tablerIcons_3 = document.createElement("script")
                    tablerIcons_3.src = "https://cdn.jsdelivr.net/npm/@tabler/icons@latest/icons-react/dist/index.umd.min.js"
                    headToAppendIframe.appendChild(tablerIcons_3) 

                    removeJs = parent.document.querySelectorAll('iframe[srcdoc*="GoogleEmoji"]')[0].parentNode
                    removeJs.style = 'display:none;'
                }} else {{
                    removeJs = parent.document.querySelectorAll('iframe[srcdoc*="GoogleEmoji"]')[0].parentNode
                    removeJs.style = 'display:none;'
                }}

            </script>
        """
        st.components.v1.html(linkJS, height=0, width=0)

    def custom_query_for_my_app_head_tag_CDN(self):

        linkJS = f"""
            <script>
                headToAppendIframe = {self.append_CDN_to}

                exists = window.top.document.querySelectorAll('link[href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@48,400,0,0"]')

                if (exists.length === 0){{
                    const GoogleEmoji = document.createElement("link");
                    GoogleEmoji.href = "https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@48,400,0,0";
                    GoogleEmoji.rel = "stylesheet";
                    headToAppendIframe.appendChild(GoogleEmoji);

                    const remixIcon = document.createElement("link");
                    remixIcon.href = "https://cdn.jsdelivr.net/npm/remixicon@3.5.0/fonts/remixicon.css";
                    remixIcon.rel = "stylesheet";
                    headToAppendIframe.appendChild(remixIcon);

                    const tablerIcons = document.createElement("link");
                    tablerIcons.href = "https://cdn.jsdelivr.net/npm/@tabler/icons@latest/iconfont/tabler-icons.min.css";
                    tablerIcons.rel = "stylesheet";
                    headToAppendIframe.appendChild(tablerIcons); 

                    const tablerIcons_2 = document.createElement("link");
                    tablerIcons_2.href ="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css";      
                    tablerIcons_2.rel = "stylesheet";
                    headToAppendIframe.appendChild(tablerIcons_2);   

                    const tablerIcons_3 = document.createElement("script")
                    tablerIcons_3.src = "https://cdn.jsdelivr.net/npm/@tabler/icons@latest/icons-react/dist/index.umd.min.js"
                    headToAppendIframe.appendChild(tablerIcons_3)

                    removeJs = parent.document.querySelectorAll('iframe[srcdoc*="GoogleEmoji"]')[0].parentNode
                    removeJs.style = 'display:none;'
                }} else {{
                    removeJs = parent.document.querySelectorAll('iframe[srcdoc*="GoogleEmoji"]')[0].parentNode
                    removeJs.style = 'display:none;'
                }}

            </script>
        """
        st.components.v1.html(linkJS, height=0, width=0)
        

# class HoverExpandSidebarTemplate:

#     """
#     Create your very own custom side bar navigation in streamlit with more ideal features. 

#     Args:
#         - (optional) backgroundColor: background color of the sidebar
#         - (optional) activeBackgroundColor: background color of active/currently clicked page/tab
#         - (optional) navigationHoverBackgroundColor: color of navigation tab when you hover over it
#         - (optional) labelIconSize: font size of the text (label) and icon
#         - (optional) distanceIconLabel: distance between the icon and the label in the navigation tab
#         (optional/required) loadPageName: manually set the page name so that it is displayed as 'active' (highlighted in the navigation tabs to show this is the current page). The component will try to seek out the page name set in the title tag of the page if this is set to None. Though for some methods in the component, if you wish to use them, this is a requirement. Methods like change_page() and load_custom_sidebar()..
#         - (required) data: data used to build the side bar navigation:
#             args:
#                 - index: required 
#                 - label: required - name of the navigation tab. The is what you want it to appear as.
#                 - iconLib: required - name of icon library. choices are -> "Remix", "Tabler", "Google"
#                 - icon: optional - icon to be used for navigation tab. icon libraries: - Google-material-symbols, - Remix icon, - Tabler Icons, - Icon-8, - line-awesome
#                 - page_name: required - name of page as set in url and also the name of the file you created via the pages folder. For example "http://localhost:8501/" would be "the name of the file" or "http://localhost:8501/data-test" would be "data-test"
#         - (optional) base_data: data used to build the base of the side bar navigation - settings, logout, socials etc:
#             args:
#                 - index: required 
#                 - label: required - name of the navigation tab. The is what you want it to appear as.
#                 - iconLib: required - name of icon library. choices are -> "Remix", "Tabler", "Google"
#                 - icon: optional - icon to be used for navigation tab. icon libraries: - Google-material-symbols, - Remix icon, - Tabler Icons, - Icon-8, - line-awesome
#                 - page_name: required - name of page as set in url and also the name of the file you created via the pages folder. For example "http://localhost:8501/" would be "the name of the file" or "http://localhost:8501/data-test" would be "data-test"

#         - (optional) webMedium: Where is this page currently being displayed. Options: "local", "streamlit-cloud", "custom" - if you are using another service like AWS etc.
#         - (optional) iframeContainer: Used to find head tag to append icon libraries so that they can be displayed. This is required if webMedium is `custom`.
#     """

#     def __init__(self, backgroundColor="black", activeBackgroundColor="white", navigationHoverBackgroundColor="rgba(255,255,255,0.35)", labelIconSizeNav="17px", labelIconSizeBase="22px", distanceIconLabel="15px", labelIconColorNotActive="#fff", labelIconColorActive="black", sizeOfCloseSidebarBtn="24px", loadPageName=None, logoImg='https://lh3.googleusercontent.com/3bXLbllNTRoiTCBdkybd1YzqVWWDRrRwJNkVRZ3mcf7rlydWfR13qJlCSxJRO8kPe304nw1jQ_B0niDo56gPgoGx6x_ZOjtVOK6UGIr3kshpmTq46pvFObfJ2K0wzoqk36MWWSnh0y9PzgE7PVSRz6Y', logoImgWidth="49px", logoText="", logoTextColor="white", logoImgHeight="49px", logoTextSize="20px", logoTextDistance="10px", data=None, base_data=None, webMedium="local", iframeContainer=None) -> None: 
       
#         self.backgroundColor = backgroundColor
#         self.activeBackgroundColor = activeBackgroundColor
#         self.navigationHoverBackgroundColor = navigationHoverBackgroundColor
#         self.labelIconSizeNav = labelIconSizeNav
#         self.labelIconSizeBase = labelIconSizeBase
#         self.distanceIconLabel = distanceIconLabel
#         self.labelIconColorNotActive = labelIconColorNotActive
#         self.labelIconColorActive = labelIconColorActive
#         self.sizeOfCloseSidebarBtn = sizeOfCloseSidebarBtn
#         self.loadPageName = loadPageName
#         self.logoImg = logoImg 
#         self.logoImgWidth = logoImgWidth
#         self.logoImgHeight = logoImgHeight
#         self.logoText = logoText
#         self.logoTextSize = logoTextSize
#         self.logoTextColor = logoTextColor
#         self.logoTextDistance = logoTextDistance
#         self.data = data
#         self.base_data = base_data
#         self.webMedium = webMedium
#         self.iframeContainer = iframeContainer

#     def sidebarCreate(self):
#         """
#         Sidebar creation component which creates the sidebar for the app.
#         """ 
        
#         js_el = f'''
                                    
#                     <script>
                        
#                         const sidebar = window.top.document.body.querySelectorAll('section[class="custom-sidebar"]');
#                         if (sidebar.length < 1){{
                            
#                             const createEL = window.top.document.createElement("section");
#                             createEL.className = 'custom-sidebar';
#                             createEL.style = "display:flex;";
#                             createElSidebarSection = document.createElement("div");
#                             createElSidebarSection.className = "sidebar-section";
#                             createElSidebarSection.style = "position:relative; padding: 1rem .8rem; width: 70px; height: 97.5vh; margin: 10px; border-radius: 0.85rem; box-shadow: rgba(50, 50, 93, 0.25) 0px 2px 5px -1px, rgba(0, 0, 0, 0.3) 0px 1px 3px -1px; background-color:{self.backgroundColor}; z-index:999991; transition: 0.5s ease; cursor:pointer; overflow:hidden;";
#                             createEL.appendChild(createElSidebarSection);

#                             const sidebarCloseBtnContainer = document.createElement("div");
#                             sidebarCloseBtnContainer.className = "close-sidebar-btn-container"
#                             sidebarCloseBtnContainer.style = "visibility:hidden; padding: 4px; border-radius: 4px; width: fit-content; z-index:999991; height:{self.sizeOfCloseSidebarBtn}; cursor:pointer; margin-top:5px;";
#                             const sidebarCloseBtn = document.createElement("div");
#                             sidebarCloseBtn.className = "close-sidebar-btn"
#                             sidebarCloseBtn.style = "font-size: {self.sizeOfCloseSidebarBtn};";
#                             const sidebarCloseBtnIcon = document.createElement("i");
#                             sidebarCloseBtnIcon.id = "close-sidebar-btn-icon"
#                             sidebarCloseBtnIcon.className = 'material-symbols-outlined';
#                             sidebarCloseBtnIcon.innerText = 'arrow_back';
#                             sidebarCloseBtnIcon.style.color = "black";

#                             sidebarCloseBtn.appendChild(sidebarCloseBtnIcon);
#                             sidebarCloseBtnContainer.appendChild(sidebarCloseBtn);

#                             createEL.appendChild(sidebarCloseBtnContainer); 
                            
#                             const body = window.top.document.body.querySelectorAll('div[data-testid="stAppViewContainer"] > section[class*="main"]'); 
#                             body[0].insertAdjacentElement('beforebegin',createEL);

#                             const newSidebar = window.top.document.body.querySelectorAll('section[class="custom-sidebar"] > div[class="sidebar-section"]');
#                             const logoImgContainer = document.createElement("div");    
#                             logoImgContainer.style = 'width:fit-content; height:50px; display:flex; justify-content:center; align-items:center;';                 

#                             const logoImg = document.createElement("img");
#                             logoImg.className = "logo-img";
#                             logoImg.src = '{self.logoImg}'; 
#                             logoImg.setAttribute("width", "{self.logoImgWidth}");
#                             logoImg.setAttribute("height", "{self.logoImgHeight}");   

#                             const logoTextDiv = document.createElement("div");
#                             logoTextDiv.className = "logo-text";
#                             logoTextDiv.innerText = '{self.logoText}';  
#                             logoTextDiv.style = "font-size: {self.logoTextSize}; color:{self.logoTextColor}; margin-left:{self.logoTextDistance}; white-space:nowrap;";           

#                             logoImgContainer.appendChild(logoImg); 
#                             logoImgContainer.appendChild(logoTextDiv); 
#                             newSidebar[0].appendChild(logoImgContainer); 

#                             const lineDivy = document.createElement('div');
#                             lineDivy.className = "divy-line-logo-nav-container";
#                             const line = document.createElement('hr');
#                             line.className="divy-line";
#                             line.style = "border-top: 0.2px solid #bbb;";
#                             lineDivy.appendChild(line);
#                             newSidebar[0].appendChild(lineDivy);

#                             const allNavigation = document.createElement("div");
#                             allNavigation.className = "all-navigation-options";
#                             allNavigation.style = "display: flex; flex-direction: column; justify-content: space-between; height: 70vh;";

#                             const navigationTabsContainer = document.createElement('ul');
#                             navigationTabsContainer.className = "navigation-selections-container";
#                             navigationTabsContainer.style = 'list-style-type:none; padding-left:0px; display:flex; flex-direction:column; width:100%; row-gap:15px;';  

#                             var pageName_ = window.top.document.location.pathname.split("/");  
#                             var pageName_ = pageName_[pageName_.length - 1];   

#                             if (pageName_ == ""){{
#                                 pageName_ = {self.data}[0]["page_name"];
#                             }} 

#                             {self.data}.forEach((el) => {{
#                                 const createListEl = document.createElement('li');
#                                 createListEl.className = "label-icon-container";  
#                                 createListEl.style = "cursor: pointer; border-radius: 4px; cursor: pointer; display:flex; align-items: center; padding: 12px; width:100%; height:49px;";

#                                 if ("{self.loadPageName}" === "None"){{
                                                                            
#                                     if (el.page_name === pageName_){{
#                                         createListEl.id = "active-element";   
#                                         createListEl.style = 'background-color:{self.activeBackgroundColor} !important; border-radius: 4px; cursor: pointer; display: flex; align-items: center; padding: 12px; width: 100%; height: 49px;';                                  
#                                     }} 
                                
#                                 }} else {{
                                    
#                                     if (el.page_name === "{self.loadPageName}"){{
#                                         createListEl.id = "active-element";   
#                                         createListEl.style = 'overflow:hidden; background-color:{self.activeBackgroundColor} !important; border-radius: 4px; cursor: pointer; display: flex; align-items: center; padding: 12px; width: 100%; height: 49px;';                                                                                                 
                                        
#                                     }} 

#                                 }}

#                                 if (el.icon && el.iconLib !== "Google"){{
#                                     const iconEl = document.createElement('i');
#                                     iconEl.className = el.icon;
#                                     iconEl.id = 'sidebar-element-icons';
#                                     iconEl.style.fontSize = "{self.labelIconSizeNav}";
#                                     iconEl.style.color = "{self.labelIconColorNotActive}";
#                                     createListEl.appendChild(iconEl);
#                                 }} else if (el.icon && el.iconLib === "Google"){{
#                                     const iconEl = document.createElement('i');
#                                     iconEl.className = 'material-symbols-outlined';
#                                     iconEl.id = 'sidebar-element-icons';
#                                     iconEl.innerText = el.icon;
#                                     iconEl.style.fontSize = "22px";
#                                     iconEl.style.color = "{self.labelIconColorNotActive}";
#                                     createListEl.appendChild(iconEl);
#                                 }}

#                                 const labelEl = document.createElement('div');
#                                 labelEl.className = "navigation-label";
#                                 labelEl.dataset.testid = el.page_name;
#                                 labelEl.innerHTML = el.label;
#                                 labelEl.style = "white-space:nowrap; display:table-cell; color:{self.labelIconColorNotActive}; font-size:{self.labelIconSizeNav}; margin-left:{self.distanceIconLabel};";
#                                 createListEl.appendChild(labelEl);
                                    
#                                 navigationTabsContainer.appendChild(createListEl);

#                             }})
#                             allNavigation.appendChild(navigationTabsContainer);
#                             newSidebar[0].appendChild(allNavigation);

#                             const logoutBtnContainer = document.createElement("div");
#                             logoutBtnContainer.className = "navigation-selections-container";
#                             logoutBtnContainer.style = 'display:flex; flex-direction:column; align-items:center; width:100%; row-gap:15px;';

#                             {self.base_data}.length > 0 && {self.base_data}.forEach((el) => {{ 
                                                        
#                                 const baseContainer = document.createElement("div");
#                                 baseContainer.className = "label-icon-container";
#                                 baseContainer.style = "cursor: pointer; border-radius: 4px; cursor: pointer; display:flex; align-items: center; padding: 12px; width:100%; height:49px;";

#                                 if ("{self.loadPageName}" === "None"){{
                                                                            
#                                     if (el.page_name === pageName_){{
#                                         baseContainer.id = "active-element";   
#                                         baseContainer.style = 'background-color:{self.activeBackgroundColor} !important; color: {self.activeBackgroundColor} !important;';
#                                     }} 
                                
#                                 }} else {{
                                    
#                                     if (el.page_name === "{self.loadPageName}"){{
#                                         baseContainer.id = "active-element";   
#                                         baseContainer.style = 'background-color:{self.activeBackgroundColor} !important; color: {self.activeBackgroundColor} !important;';
                                        
#                                     }} 

#                                 }}

#                                 const baseContainerIcon = document.createElement("i");
#                                 const baseContainerLabel = document.createElement("div");
#                                 if (el.icon && el.iconLib !== "Google"){{
                                    
#                                     baseContainerIcon.className = el.icon;
#                                     baseContainerIcon.id = 'sidebar-element-icons';
#                                     baseContainerIcon.style.fontSize = "{self.labelIconSizeBase}";
#                                     baseContainerIcon.style.color = "{self.labelIconColorNotActive}";
#                                     baseContainerIcon.style.cursor= "pointer"; 
#                                     baseContainer.appendChild(baseContainerIcon);

#                                 }} else if (el.icon && el.iconLib === "Google"){{
                                
#                                     baseContainerIcon.className = 'material-symbols-outlined';
#                                     baseContainerIcon.id = 'sidebar-element-icons';
#                                     baseContainerIcon.innerText = el.icon;
#                                     baseContainerIcon.style.fontSize = "{self.labelIconSizeBase}";
#                                     baseContainerIcon.style.color = "{self.labelIconColorNotActive}";
#                                     baseContainerIcon.style.cursor= "pointer"; 
#                                     baseContainer.appendChild(baseContainerIcon);
                                    
#                                 }}

#                                 baseContainerLabel.className = "navigation-label";  
#                                 baseContainerLabel.style = "white-space:nowrap; display:table-cell; color:{self.labelIconColorNotActive}; font-size:{self.labelIconSizeBase}; margin-left:{self.distanceIconLabel};";
#                                 baseContainerLabel.innerText = el.label;
#                                 baseContainerLabel.dataset.testid = el.page_name;
#                                 baseContainer.appendChild(baseContainerLabel);

#                                 logoutBtnContainer.appendChild(baseContainer);

#                             }})

#                             allNavigation.appendChild(logoutBtnContainer); 
#                             newSidebar[0].appendChild(allNavigation);    
                            
#                         }}
                    
#                     </script> 

#                 '''
        
#         st.components.v1.html(js_el, height=0, width=0) 

#         st.html(
#             f'''
#                 <style>

#                    \*  #active-element > #sidebar-element-icons {{
#                         color: {self.labelIconColorActive} !important;                    
#                     }}

#                     #active-element > .navigation-label{{
#                         color: {self.labelIconColorActive} !important;                    
#                     }} *\

#                     .label-icon-container:hover {{
#                         background-color: {self.navigationHoverBackgroundColor};                    
#                     }}

#                     .label-icon-container:hover > #sidebar-element-icons {{
#                         color: {self.labelIconColorActive} !important;                    
#                     }}

#                     .label-icon-container:hover > .navigation-label {{
#                         color: {self.labelIconColorActive} !important;                    
#                     }}

#                     @media(hover:hover) and (min-width: 1024px){{

#                         .sidebar-section:hover{{
#                             width: 300px !important;
#                         }}
#                     }}

#                     @media (max-width: 1023px){{
                    
#                         .sidebar-section{{
#                             width: 300px !important;
#                             transform: translateX(0px) !important;
#                             transition: transform 300ms ease 0s, width 100ms ease 0s !important;
#                         }}
                    
#                         .sidebar-section.sidebar-closed{{
#                             width: 0px !important;
#                             padding: 0px !important;
#                             transform: translateX(-310px) !important;
#                             margin-left: -10px !important;
#                             transition: transform 300ms ease 0s, width 300ms ease 0s, margin-left 300ms ease 0s !important;
#                         }}
                    
#                         .close-sidebar-btn-container{{
#                             visibility:visible !important;
#                         }}
#                     }}

#                 </style>
#             '''
#         )


#     def active_navigation(self):
#         """
#             Configures the active navigation tabs - adds `active-element` id if tab is clicked, removes active style to tab clicked off and sets active style to newly clicked tab.
#         """

#         js_el = f'''
                    
#                     <script>
#                         var navigationTabs = window.top.document.querySelectorAll(".custom-sidebar > .sidebar-section > .all-navigation-options .label-icon-container"); 
#                         navigationTabs.forEach((c) => {{
#                             c.addEventListener("click", (e) => {{
                                
#                                 window.top.document.querySelectorAll('#active-element')[0]?.removeAttribute('style');
#                                 window.top.document.querySelectorAll('#active-element')[0]?.removeAttribute('id'); 
#                                 c.id = "active-element";
#                                 c.style = "background-color:{self.activeBackgroundColor} !important; border-radius: 4px; cursor: pointer; display: flex; align-items: center; padding: 12px; width: 100%; height: 49px;";

#                             }});
#                         }});

#                         let iframeScreenComp = window.top.document.querySelectorAll('iframe[srcdoc*="navigationTabs"]');
#                         iframeScreenComp[0].parentNode.style.display = "none";
                        
#                     </script>

#                 '''
#         st.components.v1.html(js_el, height=0, width=0)
      
#     def close_sidebar(self):

#         js_el_ = '''
#                     <script>
#                         function changeClassNameForSidebar (event) {
                            
#                             const sidebarSectionOpen = window.top.document.body.querySelectorAll('section[class="custom-sidebar"] > div[class="sidebar-section"]');

#                             if (sidebarSectionOpen.length > 0){
#                                 sidebarSectionOpen[0].className = "sidebar-section sidebar-closed"
#                                 const sidebarSectionCloseBtn = window.top.document.body.querySelectorAll('section[class="custom-sidebar"] > div[class="close-sidebar-btn-container"] > div[class="close-sidebar-btn"] > i');
#                                 sidebarSectionCloseBtn[0].innerText = "arrow_forward";
                                
#                             } else {
#                                 const sidebarSectionClosed = window.top.document.body.querySelectorAll('section[class="custom-sidebar"] > div[class="sidebar-section sidebar-closed"]');
#                                 sidebarSectionClosed[0].className = "sidebar-section"
#                                 const sidebarSectionCloseBtn = window.top.document.body.querySelectorAll('section[class="custom-sidebar"] > div[class="close-sidebar-btn-container"] > div[class="close-sidebar-btn"] > i');
#                                 sidebarSectionCloseBtn[0].innerText = "arrow_back";
#                             }
#                             event.preventDefault();
#                         }

#                         const sidebarSectionCloseBtn = window.top.document.body.querySelectorAll('section[class="custom-sidebar"] > div[class="close-sidebar-btn-container"]');
#                         sidebarSectionCloseBtn[0].addEventListener('click', changeClassNameForSidebar);    
#                     </script> 

#                     '''
#         st.components.v1.html(js_el_, height=0, width=0) 
    
#     def clicked_page(self, key="testing"):
#         """
#         Get the navigation user has just clicked
#         """

#         component_value = _component_func(initialPage=self.loadPageName, key=key, default=self.loadPageName)

#         return component_value

#     def change_page(self):

#         """
#         Changes page using streamlit's native `switch_page`. If you wish to use this function, `loadPageName` is required. Cannot be None.
#         """

#         if "currentPage" not in st.session_state:
#             st.session_state["currentPage"] = self.loadPageName
#         else:
#             st.session_state["currentPage"] = self.loadPageName
        
#         if "clicked_page_" not in st.session_state:
#             st.session_state["clicked_page_"] = None

#         st.session_state["clicked_page_"] = self.clicked_page()

#         if st.session_state["clicked_page_"] != None and st.session_state["clicked_page_"] != self.loadPageName:
            
#             pages_data = self.data
#             pages_data.extend(self.base_data)
#             for i in range(len(pages_data)):
#                 pages_data[i]["index"] = i 
#             keyValList = [st.session_state["clicked_page_"]]
#             expectedResult = [d for d in pages_data if d['page_name'] in keyValList]
#             st.switch_page(expectedResult[0]["page_name_programmed"])
        
#     def load_custom_sidebar(self):
#         """
#         Salad of methods used to create final sidebar. If you wish to use this function, `loadPageName` is required. Cannot be None.
#         """

#         with st.container(height=1, border=False):
#             st.html(
#                 """
#                     <div class="sidebar-custom-execution-el"></div>
#                     <style>
#                         div[height='1']:has(div[class='sidebar-custom-execution-el']){
#                             display:none;
#                         }
#                     </style>
#                 """
#             )
          
#             emojis_load = SidebarIcons(self.iframeContainer)
#             if self.webMedium == "local":
#                 emojis_load.Load_All_CDNs()
#             elif self.webMedium == "streamlit-cloud":
#                 emojis_load.Load_All_CDNs_to_streamlit_cloud()
#             elif self.webMedium == "custom":
#                 emojis_load.custom_query_for_my_app_head_tag_CDN()

#             self.sidebarCreate() 
#             # self.active_navigation()
#             self.close_sidebar()
#             self.change_page()


class HoverExpandSidebarTemplate:

    """
    Create your very own custom side bar navigation in streamlit with more ideal features. 

    Args:
        - (required) closedOnLoad: whether the sidebar should be closed when app first loads. Defaults to false
        - (required) widthOfSidebar: width of the sidebar. Defaults to 300px.
        - (required) widthOfSidebarOnHover: width of the sidebar when hovered over. Defaults to 70px.
        - (optional) closeBtnColor: color of the close sidebar button. If "auto", it uses streamlit's text color, if not "auto" then specify a color.
        - (required) widthOfSmallScreenNavActivate: width/screen size at which smaller screen sidebar is activated. Defaults to 1024px.
        - (optional) backgroundColor: background color of the sidebar
        - (optional) activeBackgroundColor: background color of active/currently clicked page/tab
        - (optional) navigationHoverBackgroundColor: color of navigation tab when you hover over it
        - (optional) labelIconSize: font size of the text (label) and icon
        - (optional) distanceIconLabel: distance between the icon and the label in the navigation tab
        (optional/required) loadPageName: manually set the page name so that it is displayed as 'active' (highlighted in the navigation tabs to show this is the current page). The component will try to seek out the page name set in the title tag of the page if this is set to None. Though for some methods in the component, if you wish to use them, this is a requirement. Methods like change_page() and load_custom_sidebar()..
        - (required) data: data used to build the side bar navigation:
            args:
                - index: required 
                - label: required - name of the navigation tab. The is what you want it to appear as.
                - iconLib: required - name of icon library. choices are -> "Remix", "Tabler", "Google"
                - icon: optional - icon to be used for navigation tab. icon libraries: - Google-material-symbols, - Remix icon, - Tabler Icons, - Icon-8, - line-awesome
                - page_name: required - name of page as set in url and also the name of the file you created via the pages folder. For example "http://localhost:8501/" would be "the name of the file" or "http://localhost:8501/data-test" would be "pages/data-test.py"
        - (optional) base_data: data used to build the base of the side bar navigation - settings, logout, socials etc:
            args:
                - index: required 
                - label: required - name of the navigation tab. The is what you want it to appear as.
                - iconLib: required - name of icon library. choices are -> "Remix", "Tabler", "Google"
                - icon: optional - icon to be used for navigation tab. icon libraries: - Google-material-symbols, - Remix icon, - Tabler Icons, - Icon-8, - line-awesome
                - page_name: required - name of page as set in url and also the name of the file you created via the pages folder. For example "http://localhost:8501/" would be "the name of the file" or "http://localhost:8501/data-test" would be "pages/data-test.py"

        - (optional) webMedium: Where is this page currently being displayed. Options: "local", "streamlit-cloud", "custom" - if you are using another service like AWS etc.
        - (optional) iframeContainer: Used to find head tag to append icon libraries so that they can be displayed. This is required if webMedium is `custom`.
    """

    def __init__(self, closedOnLoad=False, closeBtnColor="auto", widthOfSidebar="300px", widthOfSidebarOnHover="70px", widthOfSmallScreenNavActivate="1024px", backgroundColor="black", activeBackgroundColor="white", navigationHoverBackgroundColor="rgba(255,255,255,1)", labelIconSizeNav="17px", labelIconSizeBase="22px", distanceIconLabel="15px", labelIconColorNotActive="#fff", labelIconColorActive="black", sizeOfCloseSidebarBtn="24px", loadPageName=None, logoImg='https://lh3.googleusercontent.com/3bXLbllNTRoiTCBdkybd1YzqVWWDRrRwJNkVRZ3mcf7rlydWfR13qJlCSxJRO8kPe304nw1jQ_B0niDo56gPgoGx6x_ZOjtVOK6UGIr3kshpmTq46pvFObfJ2K0wzoqk36MWWSnh0y9PzgE7PVSRz6Y', logoImgWidth="49px", logoText="", logoTextColor="white", logoImgHeight="49px", logoTextSize="20px", logoTextDistance="10px", data=None, base_data=None, webMedium="local", iframeContainer=None) -> None: 
        
        self.closeBtnColor = closeBtnColor
        self.closedOnLoad = closedOnLoad
        self.widthOfSidebar = widthOfSidebar
        self.widthOfSidebarOnHover = widthOfSidebarOnHover
        self.widthOfSmallScreenNavActivate = widthOfSmallScreenNavActivate
        self.backgroundColor = backgroundColor
        self.activeBackgroundColor = activeBackgroundColor
        self.navigationHoverBackgroundColor = navigationHoverBackgroundColor
        self.labelIconSizeNav = labelIconSizeNav
        self.labelIconSizeBase = labelIconSizeBase
        self.distanceIconLabel = distanceIconLabel
        self.labelIconColorNotActive = labelIconColorNotActive
        self.labelIconColorActive = labelIconColorActive
        self.sizeOfCloseSidebarBtn = sizeOfCloseSidebarBtn
        self.loadPageName = loadPageName
        self.logoImg = logoImg 
        self.logoImgWidth = logoImgWidth
        self.logoImgHeight = logoImgHeight
        self.logoText = logoText
        self.logoTextSize = logoTextSize
        self.logoTextColor = logoTextColor
        self.logoTextDistance = logoTextDistance
        self.data = data
        self.base_data = base_data
        self.webMedium = webMedium
        self.iframeContainer = iframeContainer

    def sidebarCreate(self):
        """
        Sidebar creation component which creates the sidebar for the app.
        """ 
        
        if self.closeBtnColor != "auto":
            closeBtnColor_ = self.closeBtnColor
        else:
            closeBtnColor_ = ""

        if self.closedOnLoad:
            className = "sidebar-section sidebar-closed"
            width = "0px"
            translateX = "-"+str(float(self.widthOfSidebar.split("px")[0]) + 10)+"px" 
            close_icon = "arrow_forward"
            padding = "0px"
            margin="0px"
        else:
            className = "sidebar-section"
            width = self.widthOfSidebar
            translateX = "0px"
            close_icon = "arrow_back"
            padding = "1rem 0.8rem"
            margin="10px"
        

        
        js_el = f'''
                                    
                    <script>
                        
                        const sidebar = window.top.document.body.querySelectorAll('section[class="custom-sidebar"]');
                        const smallScreen = window.top.matchMedia('(max-width: {self.widthOfSmallScreenNavActivate})').matches;
                        if (sidebar.length < 1){{
                            
                            const createEL = window.top.document.createElement("section");
                            createEL.className = 'custom-sidebar';
                            createEL.style = "display:flex; z-index:9999991;"; 
                            createElSidebarSection = document.createElement("div");
                            
                            if (!smallScreen){{
                                createElSidebarSection.className = "sidebar-section";
                                createElSidebarSection.style = "position:relative; padding: 1rem .8rem; width: {self.widthOfSidebarOnHover}; height: 97.5vh; margin: 10px; border-radius: 0.85rem; box-shadow: rgba(50, 50, 93, 0.25) 0px 2px 5px -1px, rgba(0, 0, 0, 0.3) 0px 1px 3px -1px; background-color:{self.backgroundColor}; z-index:999991; transition: 0.5s ease; cursor:pointer; overflow:hidden;";
                            }} else {{
                                createElSidebarSection.className = "{className}";
                                createElSidebarSection.style = 'position:relative; padding: {padding}; height: 97.5vh; margin: {margin}; border-radius: 0.85rem; box-shadow: rgba(50, 50, 93, 0.25) 0px 2px 5px -1px, rgba(0, 0, 0, 0.3) 0px 1px 3px -1px; background-color:{self.backgroundColor}; z-index:999991; cursor:pointer; overflow:hidden; width: {width}; transform: translateX({translateX}); transition: transform 300ms ease 0s, width 100ms ease 0s !important;';
                            }}
                            
                            createEL.appendChild(createElSidebarSection);

                            const sidebarCloseBtnContainer = document.createElement("div");
                            sidebarCloseBtnContainer.className = "close-sidebar-btn-container"
                            if (!smallScreen){{
                                sidebarCloseBtnContainer.style = "visibility:hidden; padding: 4px; border-radius: 4px; width: fit-content; z-index:999991; height:{self.sizeOfCloseSidebarBtn}; cursor:pointer; margin-top:5px;";
                            }} else {{
                                sidebarCloseBtnContainer.style = "visibility:visible; padding: 4px; border-radius: 4px; width: fit-content; z-index:999991; height:{self.sizeOfCloseSidebarBtn}; cursor:pointer; margin-top:5px;";
                            }}
                            
                            const sidebarCloseBtn = document.createElement("div");
                            sidebarCloseBtn.className = "close-sidebar-btn"
                            sidebarCloseBtn.style = "font-size: {self.sizeOfCloseSidebarBtn};";
                            const sidebarCloseBtnIcon = document.createElement("i");
                            sidebarCloseBtnIcon.id = "close-sidebar-btn-icon"
                            sidebarCloseBtnIcon.className = 'material-symbols-outlined';
                            if (!smallScreen){{
                                sidebarCloseBtnIcon.innerText = 'arrow_back';
                            }} else {{
                                sidebarCloseBtnIcon.innerText = '{close_icon}';
                            }}
                            
                            sidebarCloseBtnIcon.style.color = "{closeBtnColor_}";

                            sidebarCloseBtn.appendChild(sidebarCloseBtnIcon);
                            sidebarCloseBtnContainer.appendChild(sidebarCloseBtn);

                            


                            createEL.appendChild(sidebarCloseBtnContainer); 
                            
                            const body = window.top.document.body.querySelectorAll('div[data-testid="stAppViewContainer"] > section[class*="main"]'); 
                            body[0].insertAdjacentElement('beforebegin',createEL);
                            let newSidebar = ""
                            if (!smallScreen){{
                                const newSidebarS = window.top.document.body.querySelectorAll('section[class="custom-sidebar"] > div[class="sidebar-section"]');
                                newSidebar = newSidebarS
                                
                            }} else{{
                                const newSidebarS = window.top.document.body.querySelectorAll('section[class="custom-sidebar"] > div[class="{className}"]');
                                newSidebar = newSidebarS
                                
                            }}
                            
                            
                            const logoImgContainer = document.createElement("div");    
                            logoImgContainer.style = 'width:fit-content; height:50px; display:flex; justify-content:center; align-items:center;';                 

                            const logoImg = document.createElement("img");
                            logoImg.className = "logo-img";
                            logoImg.src = '{self.logoImg}'; 
                            logoImg.setAttribute("width", "{self.logoImgWidth}");
                            logoImg.setAttribute("height", "{self.logoImgHeight}");   

                            const logoTextDiv = document.createElement("div");
                            logoTextDiv.className = "logo-text";
                            logoTextDiv.innerText = '{self.logoText}';  
                            logoTextDiv.style = "font-size: {self.logoTextSize}; color:{self.logoTextColor}; margin-left:{self.logoTextDistance}; white-space:nowrap;";     
                            

                            logoImgContainer.appendChild(logoImg); 
                            logoImgContainer.appendChild(logoTextDiv); 
                            newSidebar[0].appendChild(logoImgContainer); 
                            

                            const lineDivy = document.createElement('div');
                            lineDivy.className = "divy-line-logo-nav-container";
                            const line = document.createElement('hr');
                            line.className="divy-line";
                            line.style = "border-top: 0.2px solid #bbb;";
                            lineDivy.appendChild(line);
                            newSidebar[0].appendChild(lineDivy);

                            const allNavigation = document.createElement("div"); 
                            allNavigation.className = "all-navigation-options";
                            allNavigation.style = "display: flex; flex-direction: column; justify-content: space-between; height: 70vh;";

                            const navigationTabsContainer = document.createElement('ul');
                            navigationTabsContainer.className = "navigation-selections-container";
                            navigationTabsContainer.style = 'list-style-type:none; padding-left:0px; display:flex; flex-direction:column; width:100%; row-gap:15px;';  

                            var pageName_ = window.top.document.location.pathname.split("/");  
                            var pageName_ = pageName_[pageName_.length - 1];   

                            if (pageName_ == ""){{
                                pageName_ = {self.data}[0]["page_name"];
                            }} 
                            

                            {self.data}.forEach((el) => {{
                                const createListEl = document.createElement('li');
                                createListEl.className = "label-icon-container";  
                                createListEl.style.borderRadius = "4px";
                                
                                const navTabContent = document.createElement('div');
                                navTabContent.className = "contents-container";
                                navTabContent.style = "cursor: pointer; border-radius: 4px; cursor: pointer; display:flex; align-items: center; padding: 12px; width:100%; height:49px;";
                                
                                const iconEl = document.createElement('i');
                                iconEl.style.fontSize = "{self.labelIconSizeNav}";
                                iconEl.id = 'sidebar-element-icons';

                                if (el.icon && el.iconLib !== "Google"){{
                                    
                                    iconEl.className = el.icon;
                                    
                                    
                                }} else if (el.icon && el.iconLib === "Google"){{
                                    
                                    iconEl.className = 'material-symbols-outlined';
                                    iconEl.innerText = el.icon;
                                    
                                }}

                                const labelEl = document.createElement('div');
                                labelEl.className = "navigation-label";
                                labelEl.dataset.testid = el.page_name;
                                labelEl.innerHTML = el.label;
                                labelEl.style = "white-space:nowrap; display:table-cell; font-size:{self.labelIconSizeNav}; margin-left:{self.distanceIconLabel};";
                                
                                if ("{self.loadPageName}" === "None"){{
                                                                            
                                    if (el.page_name === pageName_){{
                                        createListEl.id = "active-element";   
                                        createListEl.style.backgroundColor = '{self.activeBackgroundColor}'; 
                                        iconEl.style.color = "{self.labelIconColorActive}";
                                        labelEl.style.color = "{self.labelIconColorActive}";
                                    }} else {{
                                        iconEl.style.color = "{self.labelIconColorNotActive}";
                                        labelEl.style.color = "{self.labelIconColorNotActive}";
                                        
                                    }}
                                
                                }} else {{
                                    
                                    if (el.page_name === "{self.loadPageName}"){{
                                        createListEl.id = "active-element";   
                                        createListEl.style.backgroundColor = '{self.activeBackgroundColor}';
                                        iconEl.style.color = "{self.labelIconColorActive}";
                                        labelEl.style.color = "{self.labelIconColorActive}";
                                        
                                    }}  else {{
                                        iconEl.style.color = "{self.labelIconColorNotActive}";
                                        labelEl.style.color = "{self.labelIconColorNotActive}";
                                    }}

                                }}

                                navTabContent.appendChild(iconEl);                                
                                navTabContent.appendChild(labelEl);
                                createListEl.appendChild(navTabContent);                                    
                                navigationTabsContainer.appendChild(createListEl);

                            }})
                            allNavigation.appendChild(navigationTabsContainer);
                            newSidebar[0].appendChild(allNavigation);

                            const logoutBtnContainer = document.createElement("div");
                            logoutBtnContainer.className = "navigation-selections-container";
                            logoutBtnContainer.style = 'display:flex; flex-direction:column; width:100%; row-gap:15px;';

                            {self.base_data}.length > 0 && {self.base_data}.forEach((el) => {{ 
                                                                                    
                                const baseContainer = document.createElement("div");
                                baseContainer.className = "label-icon-container";
                                baseContainer.style.borderRadius = "4px";

                                const baseContainerContent = document.createElement('div');
                                baseContainerContent.className = "contents-container";
                                baseContainerContent.style = "cursor: pointer; border-radius: 4px; cursor: pointer; display:flex; align-items: center; padding: 12px; width:100%; height:49px;";

                                const baseContainerIcon = document.createElement("i");
                                baseContainerIcon.id = 'sidebar-element-icons'; 
                                baseContainerIcon.style.fontSize = "{self.labelIconSizeBase}";

                                if (el.icon && el.iconLib !== "Google"){{
                                    
                                    baseContainerIcon.className = el.icon;                                    
                                    
                                }} else if (el.icon && el.iconLib === "Google"){{
                                    
                                    baseContainerIcon.className = 'material-symbols-outlined';
                                    baseContainerIcon.innerText = el.icon;
                                    
                                }}

                                const baseContainerLabel = document.createElement("div");
                                baseContainerLabel.className = "navigation-label";  
                                baseContainerLabel.style = "white-space:nowrap; display:table-cell; font-size:{self.labelIconSizeBase}; margin-left:{self.distanceIconLabel};";
                                baseContainerLabel.innerText = el.label;
                                baseContainerLabel.dataset.testid = el.page_name;
                                
                                
                                if ("{self.loadPageName}" === "None"){{
                                                                            
                                    if (el.page_name === pageName_){{
                                        baseContainer.id = "active-element";   
                                        baseContainer.style.backgroundColor = '{self.activeBackgroundColor}';
                                        baseContainerIcon.style.color = "{self.labelIconColorActive}"
                                        baseContainerLabel.style.color = "{self.labelIconColorActive}"
                                    }}  else {{
                                        
                                        baseContainerIcon.style.color = "{self.labelIconColorNotActive}";
                                        baseContainerLabel.style.color = "{self.labelIconColorNotActive}"
                                    }}
                                
                                }} else {{
                                    
                                    if (el.page_name === "{self.loadPageName}"){{
                                        baseContainer.id = "active-element";   
                                        baseContainer.style.backgroundColor = '{self.activeBackgroundColor}';
                                        baseContainerIcon.style.color = "{self.labelIconColorActive}"
                                        baseContainerLabel.style.color = "{self.labelIconColorActive}"
                                    }}  else {{

                                        baseContainerIcon.style.color = "{self.labelIconColorNotActive}";
                                        baseContainerLabel.style.color = "{self.labelIconColorNotActive}"
                                    }}

                                }}
                                
                                baseContainerContent.appendChild(baseContainerIcon)
                                baseContainerContent.appendChild(baseContainerLabel);
                                baseContainer.appendChild(baseContainerContent);
                                logoutBtnContainer.appendChild(baseContainer);

                            }})

                            allNavigation.appendChild(logoutBtnContainer); 
                            newSidebar[0].appendChild(allNavigation);    
                            
                        }}
                    
                    </script> 

                '''
        
        st.components.v1.html(js_el, height=0, width=0) 
    
    def hover_over_siebar_navigations(self):

        js_el = f'''
                    <script>

                        const navigationBtn = window.top.document.querySelectorAll(".label-icon-container");
                        navigationBtn.forEach((c) => {{
                            c.addEventListener('mouseover', function(e) {{ 
                                
                                e.preventDefault();
                                c.style.backgroundColor = '{self.navigationHoverBackgroundColor}'; 

                                const textLabel = c.querySelectorAll(".navigation-label");
                                textLabel[0].style.color = '{self.labelIconColorActive}';
                                const textIcon = c.querySelectorAll("#sidebar-element-icons");
                                textIcon[0].style.color = '{self.labelIconColorActive}';
                                c.style.borderRadius = '4px';
                                
                                
                            }})

                            c.addEventListener('mouseout', function(e) {{ 
                                
                                e.preventDefault();
                                const textLabel = c.querySelectorAll(".navigation-label");
                                const textIcon = c.querySelectorAll("#sidebar-element-icons");
                                c.style.borderRadius = '4px';

                                if (c.id === "active-element"){{
                                    c.style.backgroundColor = '{self.activeBackgroundColor}';
                                    textLabel[0].style.color = '{self.labelIconColorActive}';
                                    textIcon[0].style.color = '{self.labelIconColorActive}';
                                }} else {{
                                    c.style.backgroundColor = "transparent";
                                    textLabel[0].style.color = '{self.labelIconColorNotActive}';
                                    textIcon[0].style.color = '{self.labelIconColorNotActive}';
                                }}
                                                                
                            }})

                        }})
                    </script>
                '''
        st.components.v1.html(js_el, height=0, width=0)

    def smaller_screen_render(self):

        js_el_ = f'''

                    <script>
                    
                        
                        function smallScreenStyles (event){{
                            const smallScreen = window.top.matchMedia('(max-width: {self.widthOfSmallScreenNavActivate})').matches;
                            if (smallScreen){{
                                                            
                                const sidebarEl = window.top.document.querySelectorAll("div[class='sidebar-section']");
                                sidebarEl[0].style = 'position:relative; padding: 1rem .8rem; height: 97.5vh; margin: 10px; border-radius: 0.85rem; box-shadow: rgba(50, 50, 93, 0.25) 0px 2px 5px -1px, rgba(0, 0, 0, 0.3) 0px 1px 3px -1px; background-color:{self.backgroundColor}; z-index:999991; cursor:pointer; overflow:hidden; width: {self.widthOfSidebar} !important; transform: translateX(0px) !important; transition: transform 300ms ease 0s, width 100ms ease 0s !important;';
                        
                                const sidebarBtn = window.top.document.querySelectorAll("div[class='close-sidebar-btn-container']")
                                sidebarBtn[0].style.visibility = "visible";
                                
                            }} else {{
                            
                                const sidebarEl = window.top.document.querySelectorAll("div[class='sidebar-section']");
                                sidebarEl[0].style = "position:relative; padding: 1rem .8rem; width: {self.widthOfSidebarOnHover}; height: 97.5vh; margin: 10px; border-radius: 0.85rem; box-shadow: rgba(50, 50, 93, 0.25) 0px 2px 5px -1px, rgba(0, 0, 0, 0.3) 0px 1px 3px -1px; background-color:{self.backgroundColor}; z-index:999991; transition: 0.5s ease; cursor:pointer; overflow:hidden;";
                                
                                const sidebarBtn = window.top.document.querySelectorAll("div[class='close-sidebar-btn-container']")
                                sidebarBtn[0].style.visibility = "hidden";
                                
                            }}    
                        event.preventDefault();                        
                    }}
                    window.top.addEventListener('resize', smallScreenStyles);
                    //window.top.removeEventListener('resize', smallScreenStyles);

                </script>

                '''
        st.components.v1.html(js_el_, height=0, width=0) 

    def hover_over_sidebar_(self):

        min_width = str(float(self.widthOfSmallScreenNavActivate.split("px")[0]) + 1)+"px"

        js_el_ = f'''
                <script>

                    var sidebarEl = window.parent.document.querySelectorAll(".sidebar-section");
                    sidebarEl[0].addEventListener('mouseover', function(e) {{
                                                    
                        const largeScreen = window.top.matchMedia('(min-width: {min_width})').matches;
                        
                        if (largeScreen){{
                            sidebarEl[0].style.width = "{self.widthOfSidebar}" 
                        }}
                        e.preventDefault();
                                    
                    }});
                    sidebarEl[0].addEventListener('mouseout', function(e) {{
                          
                        const largeScreen = window.top.matchMedia('(min-width: 1025px)').matches;
                        
                        if (largeScreen){{
                            sidebarEl[0].style.width = "{self.widthOfSidebarOnHover}" 
                        }}
                        e.preventDefault();
                        
                    }});     
                        
                    </script>
        '''

        st.components.v1.html(js_el_, height=0, width=0)
      
    def active_navigation(self):
        """
            Configures the active navigation tabs - adds `active-element` id if tab is clicked, removes active style to tab clicked off and sets active style to newly clicked tab.
        """

        js_el = f'''
                    
                    <script>
                        var navigationTabs = window.top.document.querySelectorAll(".custom-sidebar > .sidebar-section > .all-navigation-options .label-icon-container"); 
                        navigationTabs.forEach((c) => {{
                            c.addEventListener("click", (e) => {{
                                
                                window.top.document.querySelectorAll('#active-element')[0]?.removeAttribute('style');
                                window.top.document.querySelectorAll('#active-element')[0]?.removeAttribute('id'); 
                                c.id = "active-element";
                                c.style.backgroundColor = "{self.activeBackgroundColor}";
                                c.style.borderRadius = "4px";

                                const icons_ = c.querySelectorAll(".contents-container > #sidebar-element-icons")
                                icons_[0].style.color = "{self.labelIconColorActive}";
                                const label_ = c.querySelectorAll(".contents-container > .navigation-label")
                                label_[0].style.color = "{self.labelIconColorActive}";

                                var newNavigationTabs = window.top.document.querySelectorAll(".custom-sidebar > .sidebar-section > .all-navigation-options .label-icon-container"); 
                                newNavigationTabs.forEach((c) => {{ 
                                    
                                    console.log(c.id)
                                    if (c.id !== "active-element"){{
                                        const icons_ = c.querySelectorAll(".contents-container > #sidebar-element-icons")
                                        icons_[0].style.color = "{self.labelIconColorNotActive}";
                                        const label_ = c.querySelectorAll(".contents-container > .navigation-label")
                                        label_[0].style.color = "{self.labelIconColorNotActive}";
                                    }}
                                }})

                            }});
                           
                        }});

                        let iframeScreenComp = window.top.document.querySelectorAll('iframe[srcdoc*="navigationTabs"]');
                        iframeScreenComp[0].parentNode.style.display = "none";
                        
                    </script>

                '''
        st.components.v1.html(js_el, height=0, width=0)
      
    def close_sidebar(self):

        js_el_ = f'''
                    <script>
                        function changeClassNameForSidebar (event) {{
                            
                            const sidebarSectionOpen = window.top.document.body.querySelectorAll('section[class="custom-sidebar"] > div[class="sidebar-section"]');

                            if (sidebarSectionOpen.length > 0){{
                                sidebarSectionOpen[0].className = "sidebar-section sidebar-closed"
                                sidebarSectionOpen[0].style = 'width: 0px; padding: 0px; transform: translateX(-310px); margin-left: 0px; transition: transform 300ms ease 0s, width 300ms ease 0s, margin-left 300ms ease 0s;'
                                const sidebarSectionCloseBtn = window.top.document.body.querySelectorAll('section[class="custom-sidebar"] > div[class="close-sidebar-btn-container"] > div[class="close-sidebar-btn"] > i');
                                sidebarSectionCloseBtn[0].innerText = "arrow_forward";
                                
                            }} else {{
                                const sidebarSectionClosed = window.top.document.body.querySelectorAll('section[class="custom-sidebar"] > div[class="sidebar-section sidebar-closed"]');
                                sidebarSectionClosed[0].className = "sidebar-section"
                                sidebarSectionClosed[0].style = 'position:relative; padding: 1rem .8rem; height: 97.5vh; margin: 10px; border-radius: 0.85rem; box-shadow: rgba(50, 50, 93, 0.25) 0px 2px 5px -1px, rgba(0, 0, 0, 0.3) 0px 1px 3px -1px; background-color:{self.backgroundColor}; z-index:999991; cursor:pointer; overflow:hidden; width: {self.widthOfSidebar}; transform: translateX(0px); transition: transform 300ms ease 0s, width 100ms ease 0s !important;';
                                const sidebarSectionCloseBtn = window.top.document.body.querySelectorAll('section[class="custom-sidebar"] > div[class="close-sidebar-btn-container"] > div[class="close-sidebar-btn"] > i');
                                sidebarSectionCloseBtn[0].innerText = "arrow_back";
                            }}
                            event.preventDefault();
                        }}

                        const sidebarSectionCloseBtn = window.top.document.body.querySelectorAll('section[class="custom-sidebar"] > div[class="close-sidebar-btn-container"]');
                        sidebarSectionCloseBtn[0].addEventListener('click', changeClassNameForSidebar);    
                    </script> 

                    '''
        st.components.v1.html(js_el_, height=0, width=0) 
    
    def openCloseButtonAutoColor(self):

        st.html(
            '''
                <style>
                    i[id="close-sidebar-btn-icon"]{
                        color: var(--default-textColor) !important;
                    } 
                </style>
            '''
        )

    def clicked_page(self, key="testing"):
        """
        Get the navigation user has just clicked
        """

        component_value = _component_func(initialPage=self.loadPageName, key=key, default=self.loadPageName)

        return component_value

    def change_page(self):

        """
        Changes page using streamlit's native `switch_page`. If you wish to use this function, `loadPageName` is required. Cannot be None.
        """

        if "currentPage" not in st.session_state:
            st.session_state["currentPage"] = self.loadPageName
        else:
            st.session_state["currentPage"] = self.loadPageName
        
        if "clicked_page_" not in st.session_state:
            st.session_state["clicked_page_"] = None

        st.session_state["clicked_page_"] = self.clicked_page()

        if st.session_state["clicked_page_"] != None and st.session_state["clicked_page_"] != self.loadPageName:
            
            pages_data = self.data
            pages_data.extend(self.base_data)
            for i in range(len(pages_data)):
                pages_data[i]["index"] = i 
            keyValList = [st.session_state["clicked_page_"]]
            expectedResult = [d for d in pages_data if d['page_name'] in keyValList]
            st.switch_page(expectedResult[0]["page_name_programmed"])
        
    def load_custom_sidebar(self):
        """
        Salad of methods used to create final sidebar. If you wish to use this function, `loadPageName` is required. Cannot be None.
        """

        with st.container(height=1, border=False):
            st.html(
                """
                    <div class="sidebar-custom-execution-el"></div>
                    <style>
                        div[height='1']:has(div[class='sidebar-custom-execution-el']){
                            display:none;
                        }
                    </style>
                """
            )
          
            emojis_load = SidebarIcons(self.iframeContainer)
            if self.webMedium == "local":
                emojis_load.Load_All_CDNs()
            elif self.webMedium == "streamlit-cloud":
                emojis_load.Load_All_CDNs_to_streamlit_cloud()
            elif self.webMedium == "custom":
                emojis_load.custom_query_for_my_app_head_tag_CDN()

            self.sidebarCreate() 
            self.hover_over_siebar_navigations()
            self.active_navigation()
            self.close_sidebar()
            if self.closeBtnColor == "auto":
                self.openCloseButtonAutoColor()
            self.smaller_screen_render()
            self.hover_over_sidebar_()
            self.change_page()


class NoHoverExpandSidebarTemplate:

    """
    Create your very own custom side bar navigation in streamlit with more ideal features. 

    Args:
        - (required) closedOnLoad: whether the sidebar should be closed when app first loads. Defaults to false
        - (required) widthOfSidebar: width of the sidebar. Defaults to 300px.
        - (optional) closeBtnColor: color of the close sidebar button. If "auto", it uses streamlit's text color, if not "auto" then specify a color.
        - (optional) backgroundColor: background color of the sidebar
        - (optional) activeBackgroundColor: background color of active/currently clicked page/tab
        - (optional) navigationHoverBackgroundColor: color of navigation tab when you hover over it
        - (optional) labelIconSize: font size of the text (label) and icon
        - (optional) distanceIconLabel: distance between the icon and the label in the navigation tab
        - (optional/required) loadPageName: manually set the page name so that it is displayed as 'active' (highlighted in the navigation tabs to show this is the current page). The component will try to seek out the page name set in the title tag of the page if this is set to None. Though for some methods in the component, if you wish to use them, this is a requirement. Methods like change_page() and load_custom_sidebar()..
        - (required) data: data used to build the side bar navigation:
            args:
                - index: required 
                - label: required - name of the navigation tab. The is what you want it to appear as.
                - iconLib: required - name of icon library. choices are -> "Remix", "Tabler", "Google"
                - icon: optional - icon to be used for navigation tab. icon libraries: - Google-material-symbols, - Remix icon, - Tabler Icons, - Icon-8, - line-awesome
                - page_name: required - name of page as set in url and also the name of the file you created via the pages folder. For example "http://localhost:8501/" would be "the name of the file" or "http://localhost:8501/data-test" would be "pages/data-test.py"
        - (optional) base_data: data used to build the base of the side bar navigation - settings, logout, socials etc:
            args:
                - index: required 
                - label: required - name of the navigation tab. The is what you want it to appear as.
                - iconLib: required - name of icon library. choices are -> "Remix", "Tabler", "Google"
                - icon: optional - icon to be used for navigation tab. icon libraries: - Google-material-symbols, - Remix icon, - Tabler Icons, - Icon-8, - line-awesome
                - page_name: required - name of page as set in url and also the name of the file you created via the pages folder. For example "http://localhost:8501/" would be "the name of the file" or "http://localhost:8501/data-test" would be "pages/data-test.py"

        - (optional) webMedium: Where is this page currently being displayed. Options: "local", "streamlit-cloud", "custom" - if you are using another service like AWS etc.
        - (optional) iframeContainer: Used to find head tag to append icon libraries so that they can be displayed. This is required if webMedium is `custom`.
    """

    def __init__(self, closedOnLoad=False, widthOfSidebar="300px", closeBtnColor="auto", backgroundColor="black", activeBackgroundColor="white", navigationHoverBackgroundColor="rgba(255,255,255,1)", labelIconSizeNav="17px", labelIconSizeBase="22px", distanceIconLabel="15px", labelIconColorNotActive="#fff", labelIconColorActive="black", sizeOfCloseSidebarBtn="24px", loadPageName=None, logoImg='https://lh3.googleusercontent.com/3bXLbllNTRoiTCBdkybd1YzqVWWDRrRwJNkVRZ3mcf7rlydWfR13qJlCSxJRO8kPe304nw1jQ_B0niDo56gPgoGx6x_ZOjtVOK6UGIr3kshpmTq46pvFObfJ2K0wzoqk36MWWSnh0y9PzgE7PVSRz6Y', logoImgWidth="49px", logoText="", logoTextColor="white", logoImgHeight="49px", logoTextSize="20px", logoTextDistance="10px", data=None, base_data=None, webMedium="local", iframeContainer=None) -> None: 
        

        self.closedOnLoad = closedOnLoad
        self.widthOfSidebar = widthOfSidebar
        self.closeBtnColor = closeBtnColor
        self.backgroundColor = backgroundColor
        self.activeBackgroundColor = activeBackgroundColor
        self.navigationHoverBackgroundColor = navigationHoverBackgroundColor
        self.labelIconSizeNav = labelIconSizeNav
        self.labelIconSizeBase = labelIconSizeBase
        self.distanceIconLabel = distanceIconLabel
        self.labelIconColorNotActive = labelIconColorNotActive
        self.labelIconColorActive = labelIconColorActive
        self.sizeOfCloseSidebarBtn = sizeOfCloseSidebarBtn
        self.loadPageName = loadPageName
        self.logoImg = logoImg 
        self.logoImgWidth = logoImgWidth
        self.logoImgHeight = logoImgHeight
        self.logoText = logoText
        self.logoTextSize = logoTextSize
        self.logoTextColor = logoTextColor
        self.logoTextDistance = logoTextDistance
        self.data = data
        self.base_data = base_data
        self.webMedium = webMedium
        self.iframeContainer = iframeContainer

    def sidebarCreate(self):
        """
        Sidebar creation component which creates the sidebar for the app.
        """ 
        if self.closeBtnColor != "auto":
            closeBtnColor_ = self.closeBtnColor
        else:
            closeBtnColor_ = ""

        if self.closedOnLoad:
            className = "sidebar-section sidebar-closed"
            width = "0px"
            translateX = "-"+str(float(self.widthOfSidebar.split("px")[0]) + 10)+"px" 
            close_icon = "arrow_forward"
            padding = "0px"
            margin="0px"
        else:
            className = "sidebar-section"
            width = self.widthOfSidebar
            translateX = "0px"
            close_icon = "arrow_back"
            padding = "1rem 0.8rem"
            margin="10px"
        
        js_el = f'''
                                    
                    <script>
                        
                        const sidebar = window.top.document.body.querySelectorAll('section[class="custom-sidebar"]');
                        if (sidebar.length < 1){{
                            
                            const createEL = window.top.document.createElement("section");
                            createEL.className = 'custom-sidebar';
                            createEL.style = "display:flex; z-index:9999991;";
                            createElSidebarSection = document.createElement("div");
                            createElSidebarSection.className = "{className}";
                            
                            createElSidebarSection.style = 'position:relative; padding: {padding}; height: 97.5vh; margin: {margin}; border-radius: 0.85rem; box-shadow: rgba(50, 50, 93, 0.25) 0px 2px 5px -1px, rgba(0, 0, 0, 0.3) 0px 1px 3px -1px; background-color:{self.backgroundColor}; z-index:999991; cursor:pointer; overflow:hidden; width: {width}; transform: translateX({translateX}); transition: transform 300ms ease 0s, width 100ms ease 0s !important;';
                            
                            
                            createEL.appendChild(createElSidebarSection);

                            const sidebarCloseBtnContainer = document.createElement("div");
                            sidebarCloseBtnContainer.className = "close-sidebar-btn-container"
                            sidebarCloseBtnContainer.style = "visibility:visible; padding: 4px; border-radius: 4px; width: fit-content; z-index:999991; height:{self.sizeOfCloseSidebarBtn}; cursor:pointer; margin-top:5px;";
                            
                            const sidebarCloseBtn = document.createElement("div");
                            sidebarCloseBtn.className = "close-sidebar-btn"
                            sidebarCloseBtn.style = "font-size: {self.sizeOfCloseSidebarBtn};";
                            const sidebarCloseBtnIcon = document.createElement("i");
                            sidebarCloseBtnIcon.id = "close-sidebar-btn-icon"
                            sidebarCloseBtnIcon.className = 'material-symbols-outlined';
                            sidebarCloseBtnIcon.innerText = '{close_icon}';
                            sidebarCloseBtnIcon.style.color = "{closeBtnColor_}";

                            sidebarCloseBtn.appendChild(sidebarCloseBtnIcon);
                            sidebarCloseBtnContainer.appendChild(sidebarCloseBtn);


                            createEL.appendChild(sidebarCloseBtnContainer); 
                            
                            const body = window.top.document.body.querySelectorAll('div[data-testid="stAppViewContainer"] > section[class*="main"]'); 
                            body[0].insertAdjacentElement('beforebegin',createEL);

                            const newSidebar = window.top.document.body.querySelectorAll('section[class="custom-sidebar"] > div[class="{className}"]');
                            const logoImgContainer = document.createElement("div");    
                            logoImgContainer.style = 'width:fit-content; height:50px; display:flex; justify-content:center; align-items:center;';                 

                            const logoImg = document.createElement("img");
                            logoImg.className = "logo-img";
                            logoImg.src = '{self.logoImg}'; 
                            logoImg.setAttribute("width", "{self.logoImgWidth}");
                            logoImg.setAttribute("height", "{self.logoImgHeight}");   

                            const logoTextDiv = document.createElement("div");
                            logoTextDiv.className = "logo-text";
                            logoTextDiv.innerText = '{self.logoText}';  
                            logoTextDiv.style = "font-size: {self.logoTextSize}; color:{self.logoTextColor}; margin-left:{self.logoTextDistance}; white-space:nowrap;";           

                            logoImgContainer.appendChild(logoImg); 
                            logoImgContainer.appendChild(logoTextDiv); 
                            newSidebar[0].appendChild(logoImgContainer); 

                            const lineDivy = document.createElement('div');
                            lineDivy.className = "divy-line-logo-nav-container";
                            const line = document.createElement('hr');
                            line.className="divy-line";
                            line.style = "border-top: 0.2px solid #bbb;";
                            lineDivy.appendChild(line);
                            newSidebar[0].appendChild(lineDivy);

                            const allNavigation = document.createElement("div"); 
                            allNavigation.className = "all-navigation-options";
                            allNavigation.style = "display: flex; flex-direction: column; justify-content: space-between; height: 70vh;";

                            const navigationTabsContainer = document.createElement('ul');
                            navigationTabsContainer.className = "navigation-selections-container";
                            navigationTabsContainer.style = 'list-style-type:none; padding-left:0px; display:flex; flex-direction:column; width:100%; row-gap:15px;';  

                            var pageName_ = window.top.document.location.pathname.split("/");  
                            var pageName_ = pageName_[pageName_.length - 1];   

                            if (pageName_ == ""){{
                                pageName_ = {self.data}[0]["page_name"];
                            }} 
                            

                            {self.data}.forEach((el) => {{
                                const createListEl = document.createElement('li');
                                createListEl.className = "label-icon-container";  
                                createListEl.style.borderRadius = "4px";
                                
                                const navTabContent = document.createElement('div');
                                navTabContent.className = "contents-container";
                                navTabContent.style = "cursor: pointer; border-radius: 4px; cursor: pointer; display:flex; align-items: center; padding: 12px; width:100%; height:49px;";
                                
                                const iconEl = document.createElement('i');
                                iconEl.style.fontSize = "{self.labelIconSizeNav}";
                                iconEl.id = 'sidebar-element-icons';

                                if (el.icon && el.iconLib !== "Google"){{
                                    
                                    iconEl.className = el.icon;
                                    
                                    
                                }} else if (el.icon && el.iconLib === "Google"){{
                                    
                                    iconEl.className = 'material-symbols-outlined';
                                    iconEl.innerText = el.icon;
                                    
                                }}

                                const labelEl = document.createElement('div');
                                labelEl.className = "navigation-label";
                                labelEl.dataset.testid = el.page_name;
                                labelEl.innerHTML = el.label;
                                labelEl.style = "white-space:nowrap; display:table-cell; font-size:{self.labelIconSizeNav}; margin-left:{self.distanceIconLabel}; width:100%;";
                                
                                if ("{self.loadPageName}" === "None"){{
                                                                            
                                    if (el.page_name === pageName_){{
                                        createListEl.id = "active-element";   
                                        createListEl.style.backgroundColor = '{self.activeBackgroundColor}'; 
                                        iconEl.style.color = "{self.labelIconColorActive}";
                                        labelEl.style.color = "{self.labelIconColorActive}";
                                    }} else {{
                                        iconEl.style.color = "{self.labelIconColorNotActive}";
                                        labelEl.style.color = "{self.labelIconColorNotActive}";
                                        
                                    }}
                                
                                }} else {{
                                    
                                    if (el.page_name === "{self.loadPageName}"){{
                                        createListEl.id = "active-element";   
                                        createListEl.style.backgroundColor = '{self.activeBackgroundColor}';
                                        iconEl.style.color = "{self.labelIconColorActive}";
                                        labelEl.style.color = "{self.labelIconColorActive}";
                                        
                                    }}  else {{
                                        iconEl.style.color = "{self.labelIconColorNotActive}";
                                        labelEl.style.color = "{self.labelIconColorNotActive}";
                                    }}

                                }}

                                navTabContent.appendChild(iconEl);                                
                                navTabContent.appendChild(labelEl);
                                createListEl.appendChild(navTabContent);                                    
                                navigationTabsContainer.appendChild(createListEl);

                            }})
                            allNavigation.appendChild(navigationTabsContainer);
                            newSidebar[0].appendChild(allNavigation);

                            const logoutBtnContainer = document.createElement("div");
                            logoutBtnContainer.className = "navigation-selections-container";
                            logoutBtnContainer.style = 'display:flex; flex-direction:column; width:100%; row-gap:15px;';

                            {self.base_data}.length > 0 && {self.base_data}.forEach((el) => {{ 
                                                                                    
                                const baseContainer = document.createElement("div");
                                baseContainer.className = "label-icon-container";
                                baseContainer.style.borderRadius = "4px";

                                const baseContainerContent = document.createElement('div');
                                baseContainerContent.className = "contents-container";
                                baseContainerContent.style = "cursor: pointer; border-radius: 4px; cursor: pointer; display:flex; align-items: center; padding: 12px; width:100%; height:49px;";

                                const baseContainerIcon = document.createElement("i");
                                baseContainerIcon.id = 'sidebar-element-icons'; 
                                baseContainerIcon.style.fontSize = "{self.labelIconSizeBase}";

                                if (el.icon && el.iconLib !== "Google"){{
                                    
                                    baseContainerIcon.className = el.icon;                                    
                                    
                                }} else if (el.icon && el.iconLib === "Google"){{
                                    
                                    baseContainerIcon.className = 'material-symbols-outlined';
                                    baseContainerIcon.innerText = el.icon;
                                    
                                }}

                                const baseContainerLabel = document.createElement("div");
                                baseContainerLabel.className = "navigation-label";  
                                baseContainerLabel.style = "white-space:nowrap; display:table-cell; font-size:{self.labelIconSizeBase}; margin-left:{self.distanceIconLabel};";
                                baseContainerLabel.innerText = el.label;
                                baseContainerLabel.dataset.testid = el.page_name;
                                
                                
                                if ("{self.loadPageName}" === "None"){{
                                                                            
                                    if (el.page_name === pageName_){{
                                        baseContainer.id = "active-element";   
                                        baseContainer.style.backgroundColor = '{self.activeBackgroundColor}';
                                        baseContainerIcon.style.color = "{self.labelIconColorActive}"
                                        baseContainerLabel.style.color = "{self.labelIconColorActive}"
                                    }}  else {{
                                        
                                        baseContainerIcon.style.color = "{self.labelIconColorNotActive}";
                                        baseContainerLabel.style.color = "{self.labelIconColorNotActive}"
                                    }}
                                
                                }} else {{
                                    
                                    if (el.page_name === "{self.loadPageName}"){{
                                        baseContainer.id = "active-element";   
                                        baseContainer.style.backgroundColor = '{self.activeBackgroundColor}';
                                        baseContainerIcon.style.color = "{self.labelIconColorActive}"
                                        baseContainerLabel.style.color = "{self.labelIconColorActive}"
                                    }}  else {{

                                        baseContainerIcon.style.color = "{self.labelIconColorNotActive}";
                                        baseContainerLabel.style.color = "{self.labelIconColorNotActive}"
                                    }}

                                }}
                                
                                baseContainerContent.appendChild(baseContainerIcon)
                                baseContainerContent.appendChild(baseContainerLabel);
                                baseContainer.appendChild(baseContainerContent);
                                logoutBtnContainer.appendChild(baseContainer);

                            }})

                            allNavigation.appendChild(logoutBtnContainer); 
                            newSidebar[0].appendChild(allNavigation);    
                            
                        }}
                    
                    </script> 

                '''
        
        st.components.v1.html(js_el, height=0, width=0) 
    
    def hover_over_siebar_navigations(self):

        js_el = f'''
                    <script>

                        const navigationBtn = window.top.document.querySelectorAll(".label-icon-container");
                        navigationBtn.forEach((c) => {{
                            c.addEventListener('mouseover', function(e) {{ 
                                
                                e.preventDefault();
                                c.style.backgroundColor = '{self.navigationHoverBackgroundColor}'; 

                                const textLabel = c.querySelectorAll(".navigation-label");
                                textLabel[0].style.color = '{self.labelIconColorActive}';
                                const textIcon = c.querySelectorAll("#sidebar-element-icons");
                                textIcon[0].style.color = '{self.labelIconColorActive}';
                                c.style.borderRadius = '4px';
                                
                                
                            }})

                            c.addEventListener('mouseout', function(e) {{ 
                                
                                e.preventDefault();
                                const textLabel = c.querySelectorAll(".navigation-label");
                                const textIcon = c.querySelectorAll("#sidebar-element-icons");
                                c.style.borderRadius = '4px';

                                if (c.id === "active-element"){{
                                    c.style.backgroundColor = '{self.activeBackgroundColor}';
                                    textLabel[0].style.color = '{self.labelIconColorActive}';
                                    textIcon[0].style.color = '{self.labelIconColorActive}';
                                }} else {{
                                    c.style.backgroundColor = "transparent";
                                    textLabel[0].style.color = '{self.labelIconColorNotActive}';
                                    textIcon[0].style.color = '{self.labelIconColorNotActive}';
                                }}
                                                                
                            }})

                        }})
                    </script>
                '''
        st.components.v1.html(js_el, height=0, width=0)

    def active_navigation(self):
        """
            Configures the active navigation tabs - adds `active-element` id if tab is clicked, removes active style to tab clicked off and sets active style to newly clicked tab.
        """

        js_el = f'''
                    
                    <script>
                        var navigationTabs = window.top.document.querySelectorAll(".custom-sidebar > .sidebar-section > .all-navigation-options .label-icon-container"); 
                        navigationTabs.forEach((c) => {{
                            c.addEventListener("click", (e) => {{
                                
                                window.top.document.querySelectorAll('#active-element')[0]?.removeAttribute('style');
                                window.top.document.querySelectorAll('#active-element')[0]?.removeAttribute('id'); 
                                c.id = "active-element";
                                c.style.backgroundColor = "{self.activeBackgroundColor}";
                                c.style.borderRadius = "4px";

                                const icons_ = c.querySelectorAll(".contents-container > #sidebar-element-icons")
                                icons_[0].style.color = "{self.labelIconColorActive}";
                                const label_ = c.querySelectorAll(".contents-container > .navigation-label")
                                label_[0].style.color = "{self.labelIconColorActive}";

                                var newNavigationTabs = window.top.document.querySelectorAll(".custom-sidebar > .sidebar-section > .all-navigation-options .label-icon-container"); 
                                newNavigationTabs.forEach((c) => {{ 
                                    
                                    console.log(c.id)
                                    if (c.id !== "active-element"){{
                                        const icons_ = c.querySelectorAll(".contents-container > #sidebar-element-icons")
                                        icons_[0].style.color = "{self.labelIconColorNotActive}";
                                        const label_ = c.querySelectorAll(".contents-container > .navigation-label")
                                        label_[0].style.color = "{self.labelIconColorNotActive}";
                                    }}
                                }})

                            }});
                           
                        }});

                        let iframeScreenComp = window.top.document.querySelectorAll('iframe[srcdoc*="navigationTabs"]');
                        iframeScreenComp[0].parentNode.style.display = "none";
                        
                    </script>

                '''
        st.components.v1.html(js_el, height=0, width=0)
      
    def close_sidebar(self):

        js_el_ = f'''
                    <script>
                        function changeClassNameForSidebar (event) {{
                            
                            const sidebarSectionOpen = window.top.document.body.querySelectorAll('section[class="custom-sidebar"] > div[class="sidebar-section"]');

                            if (sidebarSectionOpen.length > 0){{
                                sidebarSectionOpen[0].className = "sidebar-section sidebar-closed"
                                sidebarSectionOpen[0].style = 'width: 0px; padding: 0px; margin:0px; transform: translateX({"-"+str(float(self.widthOfSidebar.split("px")[0]) + 10)+"px"}); transition: transform 300ms ease 0s, width 300ms ease 0s;';
                                const sidebarSectionCloseBtn = window.top.document.body.querySelectorAll('section[class="custom-sidebar"] > div[class="close-sidebar-btn-container"] > div[class="close-sidebar-btn"] > i');
                                sidebarSectionCloseBtn[0].innerText = "arrow_forward";
                                
                            }} else {{
                                const sidebarSectionClosed = window.top.document.body.querySelectorAll('section[class="custom-sidebar"] > div[class="sidebar-section sidebar-closed"]');
                                sidebarSectionClosed[0].className = "sidebar-section"
                                sidebarSectionClosed[0].style = 'position:relative; padding: 1rem .8rem; height: 97.5vh; margin: 10px; border-radius: 0.85rem; box-shadow: rgba(50, 50, 93, 0.25) 0px 2px 5px -1px, rgba(0, 0, 0, 0.3) 0px 1px 3px -1px; background-color:{self.backgroundColor}; z-index:999991; cursor:pointer; overflow:hidden; width: {self.widthOfSidebar}; transform: translateX(0px); transition: transform 300ms ease 0s, width 100ms ease 0s !important;';
                                const sidebarSectionCloseBtn = window.top.document.body.querySelectorAll('section[class="custom-sidebar"] > div[class="close-sidebar-btn-container"] > div[class="close-sidebar-btn"] > i');
                                sidebarSectionCloseBtn[0].innerText = "arrow_back";
                            }}
                            event.preventDefault();
                        }}

                        const sidebarSectionCloseBtn = window.top.document.body.querySelectorAll('section[class="custom-sidebar"] > div[class="close-sidebar-btn-container"]');
                        sidebarSectionCloseBtn[0].addEventListener('click', changeClassNameForSidebar);    
                    </script> 

                    '''
        st.components.v1.html(js_el_, height=0, width=0) 
    
    def openCloseButtonAutoColor(self):

        st.html(
            '''
                <style>
                    i[id="close-sidebar-btn-icon"]{
                        color: var(--default-textColor) !important;
                    } 
                </style>
            '''
        )
    
    def clicked_page(self, key="testing"):
        """
        Get the navigation user has just clicked
        """

        component_value = _component_func(initialPage=self.loadPageName, key=key, default=self.loadPageName)

        return component_value

    def change_page(self):

        """
        Changes page using streamlit's native `switch_page`. If you wish to use this function, `loadPageName` is required. Cannot be None.
        """

        if "currentPage" not in st.session_state:
            st.session_state["currentPage"] = self.loadPageName
        else:
            st.session_state["currentPage"] = self.loadPageName
        
        if "clicked_page_" not in st.session_state:
            st.session_state["clicked_page_"] = None

        st.session_state["clicked_page_"] = self.clicked_page()

        if st.session_state["clicked_page_"] != None and st.session_state["clicked_page_"] != self.loadPageName:
            
            pages_data = self.data
            pages_data.extend(self.base_data)
            for i in range(len(pages_data)):
                pages_data[i]["index"] = i 
            keyValList = [st.session_state["clicked_page_"]]
            expectedResult = [d for d in pages_data if d['page_name'] in keyValList]
            st.switch_page(expectedResult[0]["page_name_programmed"])
        
    def load_custom_sidebar(self):
        """
        Salad of methods used to create final sidebar. If you wish to use this function, `loadPageName` is required. Cannot be None.
        """

        with st.container(height=1, border=False):
            st.html(
                """
                    <div class="sidebar-custom-execution-el"></div>
                    <style>
                        div[height='1']:has(div[class='sidebar-custom-execution-el']){
                            display:none;
                        }
                    </style>
                """
            )
          
            emojis_load = SidebarIcons(self.iframeContainer)
            if self.webMedium == "local":
                emojis_load.Load_All_CDNs()
            elif self.webMedium == "streamlit-cloud":
                emojis_load.Load_All_CDNs_to_streamlit_cloud()
            elif self.webMedium == "custom":
                emojis_load.custom_query_for_my_app_head_tag_CDN()

            self.sidebarCreate() 
            self.hover_over_siebar_navigations()
            self.active_navigation()
            self.close_sidebar()
            if self.closeBtnColor == "auto":
                self.openCloseButtonAutoColor() 
            self.change_page()

