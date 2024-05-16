import os 
import streamlit as st
from streamlit_custom_sidebar import IS_RELEASE
import streamlit.components.v1 as components


if not IS_RELEASE:
    _component_func = components.declare_component(
      
        "my_component",
        url="http://localhost:3001",
    )
else:

    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("my_component", path=build_dir)

def myComponent(initialPage="example", key="testing", default="home"):

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
        

class CustomSidebarDefault:

    """
    Create your very own custom side bar navigation in streamlit with more ideal features. 

    Args:
        - (optional) openSidebarBtnColor: color of the open sidebar button. Choose between "auto" (default) - will use streamlit default colors which change with theme change - or your own choice
        - (optional) closeSidebarBtnColor: color of the close sidebar button. Choose between "auto" (default) - will use streamlit default colors which change with theme change - or your own choice
        - (optional) backgroundColor: background color of the sidebar
        - (optional) activeBackgroundColor: background color of active/currently clicked page/tab
        - (optional) navigationHoverBackgroundColor: color of navigation tab when you hover over it
        - (optional) labelIconSize: font size of the text (label) and icon
        - (optional) distanceIconLabel: distance between the icon and the label in the navigation tab
        - (optional) closeNavOnLoad: whether or not the sidebar should be closed when the page is first rendered.
        - (optional/required) loadPageName: manually set the page name so that it is displayed as 'active' (highlighted in the navigation tabs to show this is the current page). The component will try to seek out the page name set in the title tag of the page if this is set to None. Though for some methods in the component, if you wish to use them, this is a requirement. Methods like change_page() and load_custom_sidebar().
        - (optional) serverRendering: use href links to navigate to pages instead of streamlit's extra component `switch_page`
        - (required) data: data used to build the side bar navigation:
            args:
                - index: required 
                - label: required - name of the navigation tab. The is what you want it to appear as.
                - iconLib: required - name of icon library. choices are -> "Remix", "Tabler", "Google"
                - icon: optional - icon to be used for navigation tab. icon libraries: - Google-material-symbols, - Remix icon, - Tabler Icons, - Icon-8, - line-awesome
                - page: required - name of page as set in url and also the name of the file you created via the pages folder. For example "http://localhost:8501/" would be "the name of the file" or "http://localhost:8501/data-test" would be "data-test"
                - href: optional - url to direct users to if using links to navigate to page. If `serverRendering` is True, this is required.
        - (optional) webMedium: Where is this page currently being displayed. Options: "local", "streamlit-cloud", "custom" - if you are using another service like AWS etc.
        - (optional) iframeContainer: Used to find head tag to append icon libraries so that they can be displayed. This is required if webMedium is `custom`.
    """

    def __init__(self, openSidebarBtnColor="auto", closeSidebarBtnColor="#fff", backgroundColor="black", activeBackgroundColor="rgba(255,255,255,0.5)", navigationHoverBackgroundColor="rgba(255,255,255,0.35)", labelIconSize="17px", distanceIconLabel="12px", labelIconColor="#fff", closeNavOnLoad=True, loadPageName=None, LocalOrSessionStorage=0, serverRendering=False, data=None, webMedium="local", iframeContainer=None) -> None: 
        self.openSidebarBtnColor = openSidebarBtnColor
        self.closeSidebarBtnColor = closeSidebarBtnColor
        self.backgroundColor = backgroundColor
        self.activeBackgroundColor = activeBackgroundColor
        self.navigationHoverBackgroundColor = navigationHoverBackgroundColor
        self.labelIconSize = labelIconSize
        self.distanceIconLabel = distanceIconLabel
        self.labelIconColor = labelIconColor
        self.closeNavOnLoad = closeNavOnLoad
        self.loadPageName = loadPageName
        self.serverRendering = serverRendering
        self.data = data
        self.webMedium = webMedium
        self.iframeContainer = iframeContainer 

    def sidebarCreate(self):

        if self.closeNavOnLoad:
            width = "0px"
            min_width = "0px"
            max_width = "0px"
            transform = "translateX(-336px)"
            padding="0px"
        else:
            width = "347px"
            min_width = "244px"
            max_width = "510px"
            transform = "none"
            padding="6rem 1rem"
        
        js_el = f'''
                    
                    <script>
                        
                        const sidebar = window.top.document.body.querySelectorAll('section[class="custom-sidebar"]');
                        if (sidebar.length < 1){{
                            
                            const createEL = window.top.document.createElement("section");
                            createEL.className = 'custom-sidebar';

                            createEL.style = "transition: width 300ms ease 0s, min-width 300ms ease 0s, max-width 300ms ease 0s, transform 300ms ease 0s; position:relative; height: 910px; box-sizing: border-box; flex-shrink:0; height:100vh; width:{width}; min-width:{min_width}; max-width:{max_width}; transform:{transform}; background-color:{self.backgroundColor}; z-index: 999991; padding:{padding};";
                            const body = window.top.document.body.querySelectorAll('div[data-testid="stAppViewContainer"] > section[class*="main"]'); 
                            body[0].insertAdjacentElement('beforebegin',createEL);

                            const newSidebar = window.top.document.body.querySelectorAll('section[class="custom-sidebar"]');
                            const containerForClose = document.createElement('div');
                            containerForClose.className = 'custom-sidebar-close-btn';
                            containerForClose.style = "position:absolute; top:2%; width:fit-content; right:15px; font-size:18px; cursor:pointer;";

                            if ("{self.closeSidebarBtnColor}" !== "auto"){{
                                    containerForClose.style.color = "{self.closeSidebarBtnColor}";                                        
                                }}
                            
                                const nav_emoji_close = document.createElement('i');
                                nav_emoji_close.className = 'ri-close-fill'; 
                                nav_emoji_close.id = 'close-sidebar-btn';
                                nav_emoji_close.style.padding = '0.3rem';

                                containerForClose.appendChild(nav_emoji_close)
                                newSidebar[0].appendChild(containerForClose)
                                
                                if ("{self.closeNavOnLoad}" === "False"){{
                                    const containerForOpen = document.createElement('div')
                                    containerForOpen.className = "custom-sidebar-open-button";
                                    containerForOpen.style = "height:fit-content; visibility:hidden; padding-left:5px; padding-right:5px; z-index:999990; position:absolute; top:0.5rem; width:fit-content; left:0.5rem; font-size:18px; cursor:pointer;";
                                    
                                    if ("{self.openSidebarBtnColor}" !== "auto"){{
                                        
                                        containerForOpen.style.color = "{self.openSidebarBtnColor}";

                                    }} 

                                    const nav_emoji_open = document.createElement('i');
                                    nav_emoji_open.className = 'ri-arrow-right-s-line';
                                    containerForOpen.appendChild(nav_emoji_open)
                                    body[0].insertAdjacentElement('beforebegin',containerForOpen);  
                                }} 
                                else {{

                                    const containerForOpen = document.createElement('div');
                                    containerForOpen.className = "custom-sidebar-open-button";
                                    containerForOpen.style = "height:fit-content; visibility:visible; padding-left:5px; padding-right:5px; z-index:999990; position:absolute; top:0.5rem; width:fit-content; left:0.5rem; font-size:18px; cursor:pointer;";

                                    if ("{self.openSidebarBtnColor}" !== "auto"){{
                                        containerForOpen.style.color = "{self.openSidebarBtnColor}";
                                    }}
                                
                                    const nav_emoji_open = document.createElement('i');
                                    nav_emoji_open.className = 'ri-arrow-right-s-line';
                                    containerForOpen.appendChild(nav_emoji_open);

                                    const body = window.top.document.body.querySelectorAll('div[data-testid="stAppViewContainer"] > section[class*="main"]');
                                    body[0].insertAdjacentElement('beforebegin',containerForOpen);

                                }}

                                const parentElForNav = document.createElement('div');
                                parentElForNav.className = "navigation-container";

                                const listContainer = document.createElement('ul');
                                listContainer.className = "navigation";
                                listContainer.style = "list-style-type:none; padding-left:0px; margin-bottom:0px;";

                                var pageName_ = window.top.document.location.pathname.split("/");  
                                var pageName_ = pageName_[pageName_.length - 1];   

                                if (pageName_ == ""){{
                                    pageName_ = {self.data}[0]["page_name"];
                                }}

                                {self.data}.forEach((el) => {{
                                    const createListEl = document.createElement('li');
                                    
                                    
                                    if ("{self.loadPageName}" === "None"){{
                                                                                                    
                                        if (el.page_name === pageName_){{
                                            createListEl.id = "active";
                                            createListEl.style.backgroundColor = "{self.activeBackgroundColor}";
                                            createListEl.style.borderRadius = "0.2rem";  
                                            }} 
                                    
                                    }} else {{
                                        
                                        if (el.page_name === "{self.loadPageName}"){{
                                            createListEl.id = "active";
                                            createListEl.style.backgroundColor = "{self.activeBackgroundColor}";
                                            createListEl.style.borderRadius = "0.2rem";   
                                        }} 

                                    }}

                                    const navTabContent = document.createElement('div');
                                    navTabContent.className = "contents-container";
                                    navTabContent.style = "display:flex; flex-direction:row; align-items:center; cursor:pointer; padding:3px; padding-left:4px; border-radius:0.25rem; margin-bottom:3.5px; margin-left:5px; margin-right:5px;"; 

                                    if (el.icon && el.iconLib !== "Google"){{
                                        const iconEl = document.createElement('i');
                                        iconEl.className = el.icon;
                                        iconEl.style.marginRight = "{self.distanceIconLabel}";
                                        iconEl.style.fontSize = "{self.labelIconSize}";
                                        iconEl.style.color = "{self.labelIconColor}";
                                        navTabContent.append(iconEl);
                                        //createListEl.appendChild(iconEl);
                                    }} else if (el.icon && el.iconLib === "Google"){{
                                        const iconEl = document.createElement('i');
                                        iconEl.className = 'material-symbols-outlined';
                                        iconEl.innerText = el.icon;
                                        iconEl.style.marginRight = "{self.distanceIconLabel}";
                                        iconEl.style.fontSize = "{self.labelIconSize}";
                                        iconEl.style.color = "{self.labelIconColor}";
                                        navTabContent.append(iconEl);
                                    }}

                                    const labelEl = document.createElement('span');
                                    labelEl.className = "navigation-label";
                                    labelEl.dataset.testid = el.page_name;
                                    labelEl.innerHTML = el.label;
                                    labelEl.style = "white-space:nowrap; display:table-cell;";
                                    labelEl.style.fontSize = "{self.labelIconSize}";
                                    labelEl.style.color = "{self.labelIconColor}";

                                    navTabContent.appendChild(labelEl);
                                    createListEl.append(navTabContent);
                                    
                                    listContainer.appendChild(createListEl);
                                    createListEl.className = "label-icon-container"; 
                                     
                                }})
                                
                                parentElForNav.appendChild(listContainer); 
                                newSidebar[0].appendChild(parentElForNav);
                               
                        }}
                    
                    </script> 

                '''
        st.components.v1.html(js_el, height=0, width=0)
    
    def active_navigation(self):
        """
            Configures the active navigation tabs - adds `active` id if tab is clicked, removes active style to tab clicked off and sets active style to newly clicked tab.
        """

        js_el = f'''
                    
                    <script>
                        var navigationTabs = window.top.document.querySelectorAll(".custom-sidebar > .navigation-container > .navigation > .label-icon-container");
                        navigationTabs.forEach((c) => {{
                            c.addEventListener("click", (e) => {{
                                
                                window.top.document.querySelectorAll('#active')[0]?.removeAttribute('style')
                                window.top.document.querySelectorAll('#active')[0]?.removeAttribute('id')

                                c.id = "active";
                                c.style.backgroundColor = "{self.activeBackgroundColor}";
                                c.style.cursor = "pointer";  
                                c.style.borderRadius = "0.2rem";                        
                                
                            }});
                        }});

                        let iframeScreenComp = window.top.document.querySelectorAll('iframe[srcdoc*="navigationTabs"]'); 
                        iframeScreenComp[0].parentNode.style.display = "none"; 
                       
                    </script>

                '''
        st.components.v1.html(js_el, height=0, width=0)

        css_html_ = f'''
                        <style>
                            li[class='label-icon-container']:hover{{
                                background-color: {self.navigationHoverBackgroundColor};
                                border-radius: 0.2rem;
                            }}
                            li[id='active']:hover{{
                                background-color: {self.navigationHoverBackgroundColor} !important;
                                border-radius: 0.2rem;
                            }}

                        </style>
                    '''
        st.html(css_html_)
    
    def disable_active_navigation_server_(self):
        """
        Relevant for server rendering - navigation via links. Deactivates active tab so that on click it does not redirect you back to the same page. 
        """

        custom_css = '''
                            <style>
                                li[id="active"] > a.contents-container {
                                    pointer-events: none;

                                }

                                li[id="active"] {
                                    cursor: pointer;
                                }
                            </style>
                        '''
        st.html(custom_css)
  
    def close_sidebar(self):
        """
        Configures sidebar being closed - uses streamlit native sidebar methods
        """

        js_el = f'''
                    <script>
                        
                            function closeSidebar() {{
                                const sidebar = window.top.document.body.querySelectorAll('section[class="custom-sidebar"]');
                                sidebar[0].style = "transition: width 300ms ease 0s, min-width 300ms ease 0s, max-width 300ms ease 0s, transform 900ms ease 0s; width:0px; min-width:0px; max-width:0px; transform:translateX(-336px); position:relative; height: 910px; box-sizing: border-box; flex-shrink:0; background-color:{self.backgroundColor}; z-index: 999991; padding:6rem 0px;";
                                const openNavBtn = window.top.document.body.querySelectorAll('div[class="custom-sidebar-open-button"]');
                                openNavBtn[0].style = "padding-left:5px; padding-right:5px; visibility:visible; z-index:999990; position:absolute; top:0.5rem; width:fit-content; left:0.5rem; font-size:18px; cursor:pointer;";
                                
                                if ("{self.openSidebarBtnColor}" !== "auto"){{
                                    openNavBtn[0].style.color = "{self.openSidebarBtnColor}";
                                }}
                                
                                openNavBtn[0].addEventListener('mouseover', function() {{
                                        openNavBtn[0].style = "padding-left:5px; padding-right:5px; background-color:rgba(237, 231, 225, 0.7); border-radius:6px; visibility:visible; z-index:999990; position:absolute; top:0.5rem; width:fit-content; left:0.5rem; font-size:18px; cursor:pointer;";
                            }});
                                openNavBtn[0].addEventListener('mouseout', function() {{
                                        openNavBtn[0].style = "padding-left:5px; padding-right:5px; visibility:visible; z-index:999990; position:absolute; top:0.5rem; width:fit-content; left:0.5rem; font-size:18px; cursor:pointer;";
                                }});

                            }}
                            window.top.document.querySelectorAll('.custom-sidebar-close-btn')[0].addEventListener("click", function(event) {{
                            
                                closeSidebar();
                                event.preventDefault();
                            }}, false);

                            let iframeScreenComp = window.top.document.querySelectorAll('iframe[srcdoc*="closeSidebar"]')
                            iframeScreenComp[0].parentNode.style.display = "none";
                    </script>
                '''
        st.components.v1.html(js_el, height=0, width=0)

    def open_sidebar(self):
        """
        Configures sidebar being open - uses streamlit native sidebar methods
        """

        js_el = f'''
                    <script>
                        
                            function openSidebar() {{
                                const sidebar = window.top.document.body.querySelectorAll('section[class="custom-sidebar"]');
                                sidebar[0].style = "transition: width 300ms ease 0s, min-width 300ms ease 0s, max-width 300ms ease 0s, transform 300ms ease 0s; transform:none; position:relative; height: 910px; box-sizing: border-box; flex-shrink:0; height:100vh; width:347px; min-width:244px; max-width:510px; background-color:{self.backgroundColor}; z-index: 999991; padding:6rem 1rem;";
                                const openNavBtn = window.top.document.body.querySelectorAll('div[class="custom-sidebar-open-button"]');
                                openNavBtn[0].style = "visibility:hidden;"; 

                            }}
                            window.top.document.querySelectorAll('.custom-sidebar-open-button')[0].addEventListener("click", function(event) {{
                            
                                openSidebar();
                                event.preventDefault();
                            }}, false);

                            let iframeScreenComp = window.top.document.querySelectorAll('iframe[srcdoc*="openSidebar"]')
                            iframeScreenComp[0].parentNode.style.display = "none";
                    </script>
                '''
        st.components.v1.html(js_el, height=0, width=0)
           
    def hoverOpenCloseBtnOnLoad(self):
        """
        Configures open sidebar button being being hovered on. Rendered when page is loaded and uses st.html.
        """

        st.html(
            f'''
                <style>
                    i[id='close-sidebar-btn']:hover{{
                        background-color: rgba(237, 231, 225, 0.4);
                        border-radius: 0.5rem;
                    }}

                    div[class="custom-sidebar-open-button"]:hover{{
                        background-color: rgba(237, 231, 225, 0.7);
                        color: {self.openSidebarBtnColor};
                        border-radius: 0.5rem;
                        cursor: pointer;
                    }}

                    div[class="custom-sidebar-open-button"]{{
                        color: {self.openSidebarBtnColor};
                        cursor: pointer;
                    }}
                   
                </style>
            '''
        )
    
    def openButtonAutoColor(self):
        
        st.html(
            '''
                <style>
                    div[class="custom-sidebar-open-button"]{
                        color: var(--default-textColor) !important;
                    }

                    div[class="custom-sidebar-open-button"]:hover{
                        color: var(--default-textColor) !important;
                    }

                   
                </style>
            
            '''
        )

    def closeButtonAutoColor(self):

        st.hmtl(
            '''
                <style>
                    div[class="custom-sidebar-close-btn"]{
                        color: var(--default-textColor) !important;
                    } 
                </style>
            '''
        )

        #  div[class="custom-sidebar-close-btn"]{
        #                 color: var(--default-textColor);
        #             # }
    
    def hoverActiveNavigation(self):
        """
        Create hover effect for navigation tab, using st.html
        """

        st.html(
            f'''
                <style>
                    \* li[class="label-icon-container"]:hover{{
                        background-color: {self.navigationHoverBackgroundColor}; 
                        cursor: pointer;
                    }} *\

                   \*  li[id="active"]:hover{{
                        background-color: {self.navigationHoverBackgroundColor} !important;
                    }} *\
                </style>
            '''
        )

    def hoverActiveNavigationJSExe(self):
        """
        Create hover effect for navigation tab, using javascript
        """

        js_el = f'''
                    <script>

                    var navigationTabs = window.top.document.querySelectorAll("li.label-icon-container");
                    navigationTabs.forEach((c) => {{
                            
                            c.addEventListener('mouseover', function(e) {{
                                
                                    c.style.backgroundColor = "rgba(237, 231, 225, 0.7)" 
                                }});
                            c.addEventListener('mouseout', function(e) {{

                                if (c.id === "active"){{
                                    c.style.backgroundColor = "{self.activeBackgroundColor}"
                                }} else {{
                                    c.style.backgroundColor = "transparent" 
                                }}
                                    
                                    }});
                        }} )   

                        let iframeScreenComp = window.top.document.querySelectorAll('iframe[srcdoc*="navigationTabs"]'); 
                        iframeScreenComp[0].parentNode.style.display = "none";            
                        
                    </script>

                '''
        st.components.v1.html(js_el, height=0, width=0)
                  
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

            keyValList = [st.session_state["clicked_page_"]]
            expectedResult = [d for d in self.data if d['page_name'] in keyValList]
            st.write(expectedResult)
            st.switch_page(expectedResult[0]["page_name_programmed"])    
    
    def load_custom_sidebar(self):
        """
        Salad of methods used to create final sidebar. If you wish to use this function, `loadPageName` is required. Cannot be None.
        """

        if self.loadPageName == None:
            st.error("Need to input the loadPageName parameter which is the current page this component is being loaded in.")
        else:
            with st.container(height=1, border=False):
                st.html(
                    """
                        <div class="sidebar-streamlit-template-execution-el"></div>
                        <style>
                            div[height='1']:has(div[class='sidebar-streamlit-template-execution-el']){
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
                self.hoverOpenCloseBtnOnLoad()
                self.open_sidebar()
                self.close_sidebar()
                if self.openSidebarBtnColor == "auto":
                    self.openButtonAutoColor() 
                if self.closeSidebarBtnColor == "auto":
                    self.closeButtonAutoColor()
                self.active_navigation() 
                self.change_page()


        # self.hoverActiveNavigation()
  
        
            
        # self.defaultSidebarInit()
        # self.active_navigation()
        # self.hoverOnLoad()
        # self.open_sidebar()
        # self.close_sidebar()
        # self.hoverActiveNavigation()
        # # self.hoverActiveNavigationJSExe()
        # if self.serverRendering:
        #     self.disable_active_navigation_server_()

        

