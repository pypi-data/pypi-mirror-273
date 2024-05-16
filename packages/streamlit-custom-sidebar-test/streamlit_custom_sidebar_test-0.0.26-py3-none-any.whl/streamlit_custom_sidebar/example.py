import streamlit as st
# from streamlit_custom_sidebar import Streamlit_template
# from Streamlit_template.__init__ import CustomSidebarDefault, SidebarIcons
# from streamlit_session_browser_storage import SessionStorage
# from streamlit_local_storage import LocalStorage 
# from Streamlit_template.__init__ import myComponent

st.set_page_config(layout="wide")
# sidebar_template_ = CustomSidebarDefault()


# data_ = [
#             {"index":0, "label":"Example", "page_name":"example", "page_name_programmed":"example.py", "href":"http://localhost:8501/"},
#             {"index":1, "label":"Page", "page_name":"page", "page_name_programmed":"pages/page.py", "icon":"ri-logout-box-r-line", "href":"http://localhost:8501/page"}
#         ]

# defaultSidebar = Streamlit_template.CustomSidebarDefault(closeNavOnLoad=False, backgroundColor="black", loadPageName="example", data=data_, LocalOrSessionStorage=0, serverRendering=False, webMedium="local") 
# defaultSidebar.load_custom_sidebar()


# with st.container(height=1, border=False):
#     st.html(
#         """
#             <div className="sidebar-container-init"></div>
#             <style>
#                 div[height='1']{
#                     display:none;
#                 }
#             </style>
#         """
#     )
#     defaultSidebar = CustomSidebarDefault(closeNavOnLoad=False, backgroundColor="black", loadPageName="example", data=data_, LocalOrSessionStorage=0, serverRendering=False, webMedium="local") 
#     defaultSidebar.load_custom_sidebar()
#     # defaultSidebar.change_page()

# st.write("Hiiii")

# if "clickedPage" not in st.session_state:
#     st.session_state["clickedPage"] = None 
    
# value = myComponent(default="example") #my_input_value="hello there")
# st.write("Received", value)


# # sessionS = LocalStorage(key="session_storage_init_2")
# # # sessionS.refreshItems()
# # # pageSelect = sessionS.getItem(itemKey="currentPage") 
# # pageClicked = sessionS.getItem(itemKey="clickedPage") 
# # st.write("clickedPage", pageClicked) 
# # sessionS.refreshItems()

# # st.write(st.session_state["session_storage_init_2"]) 


# # st.button("Click me")


# # if pageClicked != None and pageClicked != st.session_state["clickedPage"]:
# # st.write("previousPage", st.session_state["clickedPage"])
# # pageClicked = sessionS.getItem(itemKey="clickedPage") 
# # st.session_state["clickedPage"] = pageClicked
# # st.write( "clickedPage",pageClicked )



# # st.write("current_page", pageSelect)
# # st.write("clicked_page", pageClicked)

# # keyValList = [pageClicked]
# # expectedResult = [d for d in data_ if d['page_name'] in keyValList]
# # st.write(expectedResult)


# import streamlit as st
# # from st_screen_stats import ScreenData, StreamlitNativeWidgetScreen, WindowQuerySize, WindowQueryHelper
# # from streamlit_custom_sidebar import Streamlit_template
# # from Streamlit_template.__init__ import CustomSidebarDefault
# # from profile_sidebar.__init__ import CustomSidebarProfile  
# from slim_expand_sidebar.__init__ import CustomSidebarProfile, SidebarIcons
# # from javascript_listener import javascript_listener_frontend

# st.set_page_config(layout="wide")

# # data_ = [
# #             {"index":0, "label":"Example", "page_name":"example", "page_name_programmed":"example.py", "href":"http://localhost:8501/"},
# #             {"index":1, "label":"Page", "page_name":"page", "page_name_programmed":"pages/page.py", "icon":"ri-logout-box-r-line", "href":"http://localhost:8501/page"}
# #         ]

# # if "currentPage" not in st.session_state: # required as component will be looking for this in session state to change page via `switch_page`
# #     st.session_state["currentPage"] = data_[0] 
# # else:
# #     st.session_state["currentPage"] = data_[0] 


# # with st.container(height=1, border=False):
# #     st.html(
# #         """
# #             <div className="sidebar-container-init"></div>
# #             <style>
# #                 div[height='1']{
# #                     display:none;
# #                 }
# #             </style>
# #         """
# #     )
# #     webMedium = "local"
# #     defaultSidebar = CustomSidebarDefault(closeNavOnLoad=False, backgroundColor="black", loadPageName="example", data=data_, LocalOrSessionStorage=0, serverRendering=False, webMedium="local")
# #     defaultSidebar.load_custom_sidebar()
# #     # clicked_value_ = defaultSidebar.clicked_page(key="testing_222")
# #     clicked_value_ = javascript_listener_frontend(initialValue=None, default="example", listenerClassPatter=".custom-sidebar > .navigation-container > .navigation > .label-icon-container > .contents-container > .navigation-label") #".custom-sidebar > .all-navigation-options .label-icon-container > .navigation-label") # #active-element > .navigation-label > .navigation-label
    
# # st.write(clicked_value_)
# # # # st.write(st.session_state["currentPageClicked"])

# # if "previousPage" not in st.session_state:
# #     st.session_state["previousPage"] = "example"
# # else:
# #     st.session_state["previousPage"] = "example"

# # if "currentPage" not in st.session_state:
# #     st.session_state["currentPage"] = value_
# # else:
# #     st.session_state["currentPage"] = value_

# # st.write(st.session_state["currentPage"], st.session_state["previousPage"])







# # # with st.container(height=1, border=False):
# # #     st.html(
# # #         """
# # #             <div className="sidebar-container-init"></div>
# # #             <style>
# # #                 div[height='1']{
# # #                     display:none;
# # #                 }
# # #             </style>
# # #         """
# # #     )
# # #     defaultSidebar = CustomSidebarProfile(closeNavOnLoad=False, backgroundColor="black", loadPageName="example", data=data_, LocalOrSessionStorage=0, serverRendering=False, webMedium="local")
# # #     defaultSidebar.sidebarCreate() 

# #     # defaultSidebar.load_custom_sidebar()
# #     # value_ = defaultSidebar.clicked_page(key="testing_222")

# emojis_load = SidebarIcons(None)
# emojis_load.Load_All_CDNs()

# # # if self.webMedium == "local":
# # #     emojis_load.Load_All_CDNs()
# # # elif self.webMedium == "streamlit-cloud":
# # #     emojis_load.Load_All_CDNs_to_streamlit_cloud()
# # # elif self.webMedium == "custom":
# # #     emojis_load.custom_query_for_my_app_head_tag_CDN()


#     st.html(
#         '''
#             <style>

#                 .all-navigation-options {
#                     display: flex;
#                     flex-direction: column;
#                     justify-content: space-between;
#                     height: 70vh;
#                 }

#                 .label-icon-container{
#                     overflow:hidden;
#                     cursor: pointer;
#                     border-radius: 4px;
#                     cursor: pointer;
#                     display:flex;
#                     align-items: center;
#                     padding: 12px;
#                     width:100%;
#                     height:49px;
#                 }

#                 #active-element{
#                     overflow:hidden;
#                     background-color:white !important;
#                     border-radius: 4px;
#                     cursor: pointer;
#                     display: flex;
#                     align-items: center;
#                     padding: 12px;
#                     width: 100%;
#                     height: 49px;
#                 }

#                 #active-element > #sidebar-element-icons {
#                     color: black !important;                    
#                 }

#                 #active-element > .navigation-label{
#                     color: black !important;                    
#                 }

#                 .navigation-label{
#                     margin-left:30px;
#                 }

#                 .label-icon-container:hover {
#                     background-color: white;                    
#                 }

#                 .label-icon-container:hover > #sidebar-element-icons {
#                     color: black !important;                    
#                 }

#                 .label-icon-container:hover > .navigation-label {
#                     color: black !important;                    
#                 }

#                 .custom-sidebar{
#                     transition: 0.5s ease;
#                     position: relative;
#                     cursor:pointer;
#                 }

#                 .custom-sidebar:hover{
#                     width: 300px !important;
#                 } 

#             </style>
#         '''
#     )



# with st.container(height=1, border=False):
#     st.html(
#         '''
#             <style>
#                 div[height='1']{
#                     display:none;
#                 }
#             </style>
#         '''
#     )
#     test_sidebar_ = CustomSidebarProfile(base_data=base_data_, data=data_)
#     test_sidebar_.load_custom_sidebar()
#     # test_sidebar_.sidebarCreate()
#     # test_sidebar_.active_navigation()
#     # clicked_value_ = javascript_listener_frontend(initialValue=None, default="example", listenerClassPatter=".navigation-label") #".custom-sidebar > .all-navigation-options .label-icon-container > .navigation-label") # #active-element > .navigation-label > .navigation-label

# st.write("**Hey man**") 
# # st.write(clicked_value_) 

# import streamlit as st
# from streamlit_custom_sidebar import slim_expand_sidebar
# from slim_expand_sidebar.__init__ import HoverExpandSidebarTemplate, SidebarIcons

# st.set_page_config(layout="wide")


# if "clicked_page_" not in st.session_state:
#     st.session_state["clicked_page_"] = None

from slim_expand_sidebar.__init__ import SidebarIcons, _component_func, NoHoverExpandSidebarTemplate, HoverExpandSidebarTemplate

# st.set_page_config()

current_page = "example"

emojis_load = SidebarIcons(None)
emojis_load.Load_All_CDNs()

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

#     def __init__(self, backgroundColor="black", activeBackgroundColor="white", navigationHoverBackgroundColor="rgba(255,255,255,1)", labelIconSizeNav="17px", labelIconSizeBase="22px", distanceIconLabel="15px", labelIconColorNotActive="#fff", labelIconColorActive="black", sizeOfCloseSidebarBtn="24px", loadPageName=None, logoImg='https://lh3.googleusercontent.com/3bXLbllNTRoiTCBdkybd1YzqVWWDRrRwJNkVRZ3mcf7rlydWfR13qJlCSxJRO8kPe304nw1jQ_B0niDo56gPgoGx6x_ZOjtVOK6UGIr3kshpmTq46pvFObfJ2K0wzoqk36MWWSnh0y9PzgE7PVSRz6Y', logoImgWidth="49px", logoText="", logoTextColor="white", logoImgHeight="49px", logoTextSize="20px", logoTextDistance="10px", data=None, base_data=None, webMedium="local", iframeContainer=None) -> None: 
       
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
#                         const smallScreen = window.top.matchMedia('(max-width: 1024px)').matches;
#                         if (sidebar.length < 1){{
                            
#                             const createEL = window.top.document.createElement("section");
#                             createEL.className = 'custom-sidebar';
#                             createEL.style = "display:flex; z-index:9999991;";
#                             createElSidebarSection = document.createElement("div");
#                             createElSidebarSection.className = "sidebar-section";
#                             if (!smallScreen){{
#                                 createElSidebarSection.style = "position:relative; padding: 1rem .8rem; width: 70px; height: 97.5vh; margin: 10px; border-radius: 0.85rem; box-shadow: rgba(50, 50, 93, 0.25) 0px 2px 5px -1px, rgba(0, 0, 0, 0.3) 0px 1px 3px -1px; background-color:{self.backgroundColor}; z-index:999991; transition: 0.5s ease; cursor:pointer; overflow:hidden;";
#                             }} else {{
#                                 createElSidebarSection.style = 'position:relative; padding: 1rem .8rem; height: 97.5vh; margin: 10px; border-radius: 0.85rem; box-shadow: rgba(50, 50, 93, 0.25) 0px 2px 5px -1px, rgba(0, 0, 0, 0.3) 0px 1px 3px -1px; background-color:{self.backgroundColor}; z-index:999991; cursor:pointer; overflow:hidden; width: 300px; transform: translateX(0px); transition: transform 300ms ease 0s, width 100ms ease 0s !important;';
#                             }}
                            
#                             createEL.appendChild(createElSidebarSection);

#                             const sidebarCloseBtnContainer = document.createElement("div");
#                             sidebarCloseBtnContainer.className = "close-sidebar-btn-container"
#                             if (!smallScreen){{
#                                 sidebarCloseBtnContainer.style = "visibility:hidden; padding: 4px; border-radius: 4px; width: fit-content; z-index:999991; height:{self.sizeOfCloseSidebarBtn}; cursor:pointer; margin-top:5px;";
#                             }} else {{
#                                 sidebarCloseBtnContainer.style = "visibility:visible; padding: 4px; border-radius: 4px; width: fit-content; z-index:999991; height:{self.sizeOfCloseSidebarBtn}; cursor:pointer; margin-top:5px;";
#                             }}
                            
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
#                                 createListEl.style.borderRadius = "4px";
                                
#                                 const navTabContent = document.createElement('div');
#                                 navTabContent.className = "contents-container";
#                                 navTabContent.style = "cursor: pointer; border-radius: 4px; cursor: pointer; display:flex; align-items: center; padding: 12px; width:100%; height:49px;";
                                
#                                 const iconEl = document.createElement('i');
#                                 iconEl.style.fontSize = "{self.labelIconSizeNav}";

#                                 if (el.icon && el.iconLib !== "Google"){{
                                    
#                                     iconEl.className = el.icon;
#                                     iconEl.id = 'sidebar-element-icons';
                                    
#                                 }} else if (el.icon && el.iconLib === "Google"){{
                                    
#                                     iconEl.className = 'material-symbols-outlined';
#                                     iconEl.id = 'sidebar-element-icons';
#                                     iconEl.innerText = el.icon;
                                    
#                                 }}

#                                 const labelEl = document.createElement('div');
#                                 labelEl.className = "navigation-label";
#                                 labelEl.dataset.testid = el.page_name;
#                                 labelEl.innerHTML = el.label;
#                                 labelEl.style = "white-space:nowrap; display:table-cell; font-size:{self.labelIconSizeNav}; margin-left:{self.distanceIconLabel};";
                                
#                                 if ("{self.loadPageName}" === "None"){{
                                                                            
#                                     if (el.page_name === pageName_){{
#                                         createListEl.id = "active-element";   
#                                         createListEl.style.backgroundColor = '{self.activeBackgroundColor}'; 
#                                         iconEl.style.color = "{self.labelIconColorActive}";
#                                         labelEl.style.color = "{self.labelIconColorActive}";
#                                     }} else {{
#                                         iconEl.style.color = "{self.labelIconColorNotActive}";
#                                         labelEl.style.color = "{self.labelIconColorNotActive}";
                                        
#                                     }}
                                
#                                 }} else {{
                                    
#                                     if (el.page_name === "{self.loadPageName}"){{
#                                         createListEl.id = "active-element";   
#                                         createListEl.style.backgroundColor = '{self.activeBackgroundColor}';
#                                         iconEl.style.color = "{self.labelIconColorActive}";
#                                         labelEl.style.color = "{self.labelIconColorActive}";
                                        
#                                     }}  else {{
#                                         iconEl.style.color = "{self.labelIconColorNotActive}";
#                                         labelEl.style.color = "{self.labelIconColorNotActive}";
#                                     }}

#                                 }}

#                                 navTabContent.appendChild(iconEl);                                
#                                 navTabContent.appendChild(labelEl);
#                                 createListEl.appendChild(navTabContent);                                    
#                                 navigationTabsContainer.appendChild(createListEl);

#                             }})
#                             allNavigation.appendChild(navigationTabsContainer);
#                             newSidebar[0].appendChild(allNavigation);

#                             const logoutBtnContainer = document.createElement("div");
#                             logoutBtnContainer.className = "navigation-selections-container";
#                             logoutBtnContainer.style = 'display:flex; flex-direction:column; width:100%; row-gap:15px;';

#                             {self.base_data}.length > 0 && {self.base_data}.forEach((el) => {{ 
                                                                                    
#                                 const baseContainer = document.createElement("div");
#                                 baseContainer.className = "label-icon-container";
#                                 baseContainer.style.borderRadius = "4px";

#                                 const baseContainerContent = document.createElement('div');
#                                 baseContainerContent.className = "contents-container";
#                                 baseContainerContent.style = "cursor: pointer; border-radius: 4px; cursor: pointer; display:flex; align-items: center; padding: 12px; width:100%; height:49px;";

#                                 const baseContainerIcon = document.createElement("i");
#                                 baseContainerIcon.id = 'sidebar-element-icons'; 
#                                 baseContainerIcon.style.fontSize = "{self.labelIconSizeBase}";

#                                 if (el.icon && el.iconLib !== "Google"){{
                                    
#                                     baseContainerIcon.className = el.icon;                                    
                                    
#                                 }} else if (el.icon && el.iconLib === "Google"){{
                                    
#                                     baseContainerIcon.className = 'material-symbols-outlined';
#                                     baseContainerIcon.innerText = el.icon;
                                    
#                                 }}

#                                 const baseContainerLabel = document.createElement("div");
#                                 baseContainerLabel.className = "navigation-label";  
#                                 baseContainerLabel.style = "white-space:nowrap; display:table-cell; font-size:{self.labelIconSizeBase}; margin-left:{self.distanceIconLabel};";
#                                 baseContainerLabel.innerText = el.label;
#                                 baseContainerLabel.dataset.testid = el.page_name;
                                
                                
#                                 if ("{self.loadPageName}" === "None"){{
                                                                            
#                                     if (el.page_name === pageName_){{
#                                         baseContainer.id = "active-element";   
#                                         baseContainer.style.backgroundColor = '{self.activeBackgroundColor}';
#                                         baseContainerIcon.style.color = "{self.labelIconColorActive}"
#                                         baseContainerLabel.style.color = "{self.labelIconColorActive}"
#                                     }}  else {{
                                        
#                                         baseContainerIcon.style.color = "{self.labelIconColorNotActive}";
#                                         baseContainerLabel.style.color = "{self.labelIconColorNotActive}"
#                                     }}
                                
#                                 }} else {{
                                    
#                                     if (el.page_name === "{self.loadPageName}"){{
#                                         baseContainer.id = "active-element";   
#                                         baseContainer.style.backgroundColor = '{self.activeBackgroundColor}';
#                                         baseContainerIcon.style.color = "{self.labelIconColorActive}"
#                                         baseContainerLabel.style.color = "{self.labelIconColorActive}"
#                                     }}  else {{

#                                         baseContainerIcon.style.color = "{self.labelIconColorNotActive}";
#                                         baseContainerLabel.style.color = "{self.labelIconColorNotActive}"
#                                     }}

#                                 }}
                                
#                                 baseContainerContent.appendChild(baseContainerIcon)
#                                 baseContainerContent.appendChild(baseContainerLabel);
#                                 baseContainer.appendChild(baseContainerContent);
#                                 logoutBtnContainer.appendChild(baseContainer);

#                             }})

#                             allNavigation.appendChild(logoutBtnContainer); 
#                             newSidebar[0].appendChild(allNavigation);    
                            
#                         }}
                    
#                     </script> 

#                 '''
        
#         st.components.v1.html(js_el, height=0, width=0) 

#         # st.html(
#         #     f'''
#         #         <style>
#         #             .label-icon-container:hover {{
#         #                 background-color: {self.navigationHoverBackgroundColor}; 
#         #                 border-radius: 4px;                   
#         #             }}
#         #             .label-icon-container:hover #sidebar-element-icons {{
#         #                 color: {self.labelIconColorActive} !important;                    
#         #             }}

#         #             .label-icon-container:hover .navigation-label {{
#         #                 color: {self.labelIconColorActive} !important;                    
#         #             }}
#         #         </style>
#         #     '''
#         # )

#         # st.html(
#         #     f'''
#         #         <style>

#         #             .label-icon-container > .contents-container > #sidebar-element-icons{{
#         #                 color: {self.labelIconColorNotActive} !important;                    
#         #             }} 
#         #             .label-icon-container > .contents-container > .navigation-label{{
#         #                 color: {self.labelIconColorNotActive} !important;                    
#         #             }} 

#         #             .label-icon-container#active-element > .contents-container > #sidebar-element-icons{{
#         #                 color: {self.labelIconColorActive} !important;                      
#         #             }}
#         #             .label-icon-container#active-element > .contents-container > .navigation-label{{
#         #                 color: {self.labelIconColorActive} !important;                      
#         #             }}

#         #             .label-icon-container:hover {{
#         #                 background-color: {self.navigationHoverBackgroundColor}; 
#         #                 border-radius: 4px;                   
#         #             }}

#         #             .label-icon-container:hover #sidebar-element-icons {{
#         #                 color: {self.labelIconColorActive} !important;                    
#         #             }}

#         #             .label-icon-container:hover .navigation-label {{
#         #                 color: {self.labelIconColorActive} !important;                    
#         #             }}

#         #             @media(hover:hover) and (min-width: 1024px){{

#         #                 .sidebar-section:hover{{
#         #                     width: 300px !important;
#         #                 }}
#         #             }}

                    

                    

#         #         </style>
#         #     '''

#         #     # @media (max-width: 1023px){{
                    
#         #     #             .sidebar-section{{
#         #     #                 width: 300px !important;
#         #     #                 transform: translateX(0px) !important;
#         #     #                 transition: transform 300ms ease 0s, width 100ms ease 0s !important;
#         #     #             }}
                    
#         #     #             .sidebar-section.sidebar-closed{{
#         #     #                 width: 0px !important;
#         #     #                 padding: 0px !important;
#         #     #                 transform: translateX(-310px) !important;
#         #     #                 margin-left: -10px !important;
#         #     #                 transition: transform 300ms ease 0s, width 300ms ease 0s, margin-left 300ms ease 0s !important;
#         #     #             }}
                    
#         #     #             .close-sidebar-btn-container{{
#         #     #                 visibility:visible !important;
#         #     #             }}
#         #     #         }}

#         #     # @media (max-width: 1023px){{

#         #             #     .sidebar-section.sidebar-closed{{
#         #             #         width: 0px !important;
#         #             #         padding: 0px !important;
#         #             #         transform: translateX(-310px) !important;
#         #             #         margin-left: -10px !important;
#         #             #         transition: transform 300ms ease 0s, width 300ms ease 0s, margin-left 300ms ease 0s !important;
#         #             #     }}
                            
#         #             # }}
#         # )

#     def smaller_screen_render(self):

#         js_el_ = f'''

#                     <script>
                    
                        
#                         function smallScreenStyles (event){{
#                             const smallScreen = window.top.matchMedia('(max-width: 1024px)').matches;
#                             if (smallScreen){{
                                                            
#                                 const sidebarEl = window.top.document.querySelectorAll("div[class='sidebar-section']");
#                                 sidebarEl[0].style = 'position:relative; padding: 1rem .8rem; height: 97.5vh; margin: 10px; border-radius: 0.85rem; box-shadow: rgba(50, 50, 93, 0.25) 0px 2px 5px -1px, rgba(0, 0, 0, 0.3) 0px 1px 3px -1px; background-color:{self.backgroundColor}; z-index:999991; cursor:pointer; overflow:hidden; width: 300px !important; transform: translateX(0px) !important; transition: transform 300ms ease 0s, width 100ms ease 0s !important;';
                        
#                                 const sidebarBtn = window.top.document.querySelectorAll("div[class='close-sidebar-btn-container']")
#                                 sidebarBtn[0].style.visibility = "visible";
                                
#                             }} else {{
                            
#                                 const sidebarEl = window.top.document.querySelectorAll("div[class='sidebar-section']");
#                                 sidebarEl[0].style = "position:relative; padding: 1rem .8rem; width: 70px; height: 97.5vh; margin: 10px; border-radius: 0.85rem; box-shadow: rgba(50, 50, 93, 0.25) 0px 2px 5px -1px, rgba(0, 0, 0, 0.3) 0px 1px 3px -1px; background-color:{self.backgroundColor}; z-index:999991; transition: 0.5s ease; cursor:pointer; overflow:hidden;";
                                
#                                 const sidebarBtn = window.top.document.querySelectorAll("div[class='close-sidebar-btn-container']")
#                                 sidebarBtn[0].style.visibility = "hidden";
                                
#                             }}    
#                         event.preventDefault();                        
#                     }}
#                     window.top.addEventListener('resize', smallScreenStyles);
#                     //window.top.removeEventListener('resize', smallScreenStyles);

#                 </script>

#                 '''
#         st.components.v1.html(js_el_, height=0, width=0) 


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
#                                 c.style.backgroundColor = "{self.activeBackgroundColor}";
#                                 c.style.borderRadius = "4px";

#                                 const icons_ = c.querySelectorAll(".contents-container > #sidebar-element-icons")
#                                 icons_[0].style.color = "{self.labelIconColorActive}";
#                                 const label_ = c.querySelectorAll(".contents-container > .navigation-label")
#                                 label_[0].style.color = "{self.labelIconColorActive}";

#                                 var newNavigationTabs = window.top.document.querySelectorAll(".custom-sidebar > .sidebar-section > .all-navigation-options .label-icon-container"); 
#                                 newNavigationTabs.forEach((c) => {{ 
                                  
#                                     if (c.id !== "active-element"){{
#                                         const icons_ = c.querySelectorAll(".contents-container > #sidebar-element-icons")
#                                         icons_[0].style.color = "{self.labelIconColorNotActive}";
#                                         const label_ = c.querySelectorAll(".contents-container > .navigation-label")
#                                         label_[0].style.color = "{self.labelIconColorNotActive}";
#                                     }}
#                                 }})

#                             }});
                           
#                         }});


#                         let iframeScreenComp = window.top.document.querySelectorAll('iframe[srcdoc*="navigationTabs"]');
#                         iframeScreenComp[0].parentNode.style.display = "none";
                        
#                     </script>

#                 '''
#         st.components.v1.html(js_el, height=0, width=0)
    
#     def hover_over_siebar_navigations(self):

#         js_el = f'''
#                     <script>

#                         const navigationBtn = window.top.document.querySelectorAll(".label-icon-container");
#                         navigationBtn.forEach((c) => {{
#                             c.addEventListener('mouseover', function(e) {{ 
                                
#                                 e.preventDefault();
#                                 c.style.backgroundColor = '{self.navigationHoverBackgroundColor}'; 
#                                 c.style.borderRadius = '4px';

#                                 const textLabel = c.querySelectorAll(".navigation-label");
#                                 textLabel[0].style.color = '{self.labelIconColorActive}';
#                                 const textIcon = c.querySelectorAll("#sidebar-element-icons");
#                                 textIcon[0].style.color = '{self.labelIconColorActive}';
                                
                                
#                             }})

#                             c.addEventListener('mouseout', function(e) {{ 
                                
#                                 e.preventDefault();
#                                 const textLabel = c.querySelectorAll(".navigation-label");
#                                 const textIcon = c.querySelectorAll("#sidebar-element-icons");
#                                 c.style.borderRadius = '4px';
#                                 if (c.id === "active-element"){{
#                                     c.style.backgroundColor = '{self.activeBackgroundColor}';
#                                     textLabel[0].style.color = '{self.labelIconColorActive}';
#                                     textIcon[0].style.color = '{self.labelIconColorActive}';
#                                 }} else {{
#                                     c.style.backgroundColor = "transparent" 
#                                     textLabel[0].style.color = '{self.labelIconColorNotActive}';
#                                     textIcon[0].style.color = '{self.labelIconColorNotActive}';
#                                 }}
                                                                
#                             }})

#                         }})
#                     </script>
#                 '''
#         st.components.v1.html(js_el, height=0, width=0)

    
#     def hover_over_sidebar_(self):

#         js_el_ = f'''
#                 <script>

#                     var sidebarEl = window.parent.document.querySelectorAll(".sidebar-section");
#                     sidebarEl[0].addEventListener('mouseover', function(e) {{
                                                    
#                         const largeScreen = window.top.matchMedia('(min-width: 1025px)').matches;
                        
#                         if (largeScreen){{
#                             sidebarEl[0].style.width = "300px" 
#                         }}
                                    
#                     }});
#                     sidebarEl[0].addEventListener('mouseout', function(e) {{
                          
#                         const largeScreen = window.top.matchMedia('(min-width: 1025px)').matches;
                        
#                         if (largeScreen){{
#                             sidebarEl[0].style.width = "70px" 
#                         }}
                    
                        
#                     }});     
                        
#                     </script>
#         '''

#         st.components.v1.html(js_el_, height=0, width=0)
      

#     def close_sidebar(self):

#         js_el_ = f'''
#                     <script>
#                         function changeClassNameForSidebar (event) {{
                            
#                             const sidebarSectionOpen = window.top.document.body.querySelectorAll('section[class="custom-sidebar"] > div[class="sidebar-section"]');

#                             if (sidebarSectionOpen.length > 0){{
#                                 sidebarSectionOpen[0].className = "sidebar-section sidebar-closed"
#                                 sidebarSectionOpen[0].style = 'width: 0px; padding: 0px; transform: translateX(-310px); margin-left: 0px; transition: transform 300ms ease 0s, width 300ms ease 0s, margin-left 300ms ease 0s;'
#                                 const sidebarSectionCloseBtn = window.top.document.body.querySelectorAll('section[class="custom-sidebar"] > div[class="close-sidebar-btn-container"] > div[class="close-sidebar-btn"] > i');
#                                 sidebarSectionCloseBtn[0].innerText = "arrow_forward";
                                
#                             }} else {{
#                                 const sidebarSectionClosed = window.top.document.body.querySelectorAll('section[class="custom-sidebar"] > div[class="sidebar-section sidebar-closed"]');
#                                 sidebarSectionClosed[0].className = "sidebar-section"
#                                 sidebarSectionClosed[0].style = 'position:relative; padding: 1rem .8rem; height: 97.5vh; margin: 10px; border-radius: 0.85rem; box-shadow: rgba(50, 50, 93, 0.25) 0px 2px 5px -1px, rgba(0, 0, 0, 0.3) 0px 1px 3px -1px; background-color:{self.backgroundColor}; z-index:999991; cursor:pointer; overflow:hidden; width: 300px; transform: translateX(0px); transition: transform 300ms ease 0s, width 100ms ease 0s !important;';
#                                 const sidebarSectionCloseBtn = window.top.document.body.querySelectorAll('section[class="custom-sidebar"] > div[class="close-sidebar-btn-container"] > div[class="close-sidebar-btn"] > i');
#                                 sidebarSectionCloseBtn[0].innerText = "arrow_back";
#                             }}
#                             event.preventDefault();
#                         }}

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
#             self.hover_over_siebar_navigations()
#             self.active_navigation()
#             self.close_sidebar()
#             self.smaller_screen_render()
#             self.hover_over_sidebar_()
#             self.change_page()



data_ = [
            {"index":0, "label":"Example", "page_name":"example", "page_name_programmed":"example.py", "icon":"ri-logout-box-r-line", "href":"http://localhost:8501/"},
            {"index":1, "label":"Page", "page_name":"page", "page_name_programmed":"pages/page.py", "icon":"ri-logout-box-r-line", "href":"http://localhost:8501/page"}
        ]

base_data_ = [
    {"index":0, "label":"Settings", "page_name":"settings", "page_name_programmed":"None", "icon":"settings", "iconLib":"Google"},
    {"index":1, "label":"Logout", "page_name":"logout", "page_name_programmed":"None", "icon":"ri-logout-box-r-line", "iconLib":""}
]

test_sidebar_ = NoHoverExpandSidebarTemplate(closedOnLoad=False, base_data=base_data_, data=data_, logoText="Optum Gamer", logoTextSize="20px")
# test_sidebar_.sidebarCreate()
# test_sidebar_.active_navigation()
# test_sidebar_.smaller_screen_render()

test_sidebar_.load_custom_sidebar()
# active_navigation()

st.write("**Sup Bro**")
# st.write("**Hey Man, Bro**")

