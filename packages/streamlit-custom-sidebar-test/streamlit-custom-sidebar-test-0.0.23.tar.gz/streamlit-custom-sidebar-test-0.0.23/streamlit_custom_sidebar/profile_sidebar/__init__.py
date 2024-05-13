import os 
import streamlit as st
from streamlit_local_storage import LocalStorage
from streamlit_session_browser_storage import SessionStorage
# from streamlit_extras.switch_page_button import switch_page

import streamlit.components.v1 as components

_RELEASE = True

if not _RELEASE:
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
        

class CustomSidebarProfile:

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
        - (optional) loadPageName: manually set the page name so that it is displayed as 'active' (highlighted in the navigation tabs to show this is the current page). The component will try to seek out the page name set in the title tag of the page if this is set to None.
        - (optional) LocalOrSessionStorage: where to store the current page selected. choices are [0,1]. 0 = local storage, 1 = session storage
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
        self.storageChoice = ["localStorage", "sessionStorage"][LocalOrSessionStorage]
        self.serverRendering = serverRendering
        self.data = data
        self.webMedium = webMedium
        self.iframeContainer = iframeContainer

    def sidebarCreate(self):

        loadPageName = "None"

        
        js_el = f'''
                    
                    
                    <script>
                        
                        const sidebar = window.top.document.body.querySelectorAll('section[class="custom-sidebar"]');
                        if (sidebar.length < 1){{
                            
                            const createEL = window.top.document.createElement("section");
                            createEL.className = 'custom-sidebar';

                            createEL.style = "padding: 2rem 2.5rem; width: 320px; height: 100vh; margin-top: 5px; marginLeft: 5px; border-radius: 10px; box-shadow: rgba(50, 50, 93, 0.25) 0px 2px 5px -1px, rgba(0, 0, 0, 0.3) 0px 1px 3px -1px; background-color:white; z-index:999991";
                            const body = window.top.document.body.querySelectorAll('div[data-testid="stAppViewContainer"] > section[class*="main"]'); 
                            body[0].insertAdjacentElement('beforebegin',createEL);

                            const newSidebar = window.top.document.body.querySelectorAll('section[class="custom-sidebar"]');
                            const sidebarTopElement = document.createElement('div');
                            sidebarTopElement.className = 'logo-and-name';
                            sidebarTopElement.style = "display: flex; align-items: center; column-gap: 10px; justify-content: flex-start;";
                            const logoEl = document.createElement("img");
                            logoEl.width = '40';
                            logoEl.height = '40';
                            logoEl.src = 'https://lh3.googleusercontent.com/3bXLbllNTRoiTCBdkybd1YzqVWWDRrRwJNkVRZ3mcf7rlydWfR13qJlCSxJRO8kPe304nw1jQ_B0niDo56gPgoGx6x_ZOjtVOK6UGIr3kshpmTq46pvFObfJ2K0wzoqk36MWWSnh0y9PzgE7PVSRz6Y';
                            
                            const logoTitle = document.createElement("h4");
                            logoTitle.className = "logo-title";
                            logoTitle.style = 'font-size:18px';
                            logoTitle.innerText = 'Title Insert here';
                            
                            sidebarTopElement.appendChild(logoEl);
                            sidebarTopElement.appendChild(logoTitle);
                            newSidebar[0].appendChild(sidebarTopElement);

                            //const newSidebar = window.top.document.body.querySelectorAll('section[class="custom-sidebar"]'); 
                            const SearchBarContainer = document.createElement("div");
                            SearchBarContainer.style = 'display: flex; justify-content: flex-start; align-items:center; width: calc(100% - 1px); margin-top: 50px; margin-bottom: 40px; box-shadow:rgba(50, 50, 93, 0.25) 0px 2px 5px -1px, rgba(0, 0, 0, 0.3) 0px 1px 3px -1px; border-radius:7px;';
                            const searchIcon = document.createElement("i");
                            searchIcon.className = 'ri-search-line';
                            const SearchBar = document.createElement("input");
                            SearchBar.className = 'sidebar-search-bar';
                            SearchBar.style.border = 'none';
                            SearchBarContainer.appendChild(searchIcon)
                            SearchBarContainer.appendChild(SearchBar);
                            newSidebar[0].appendChild(SearchBarContainer);

                            const navigationSelectionsContainer = document.createElement("div");
                            const navigationSelections = document.createElement("ul");
                            navigationSelections.style = "display: flex; flex-direction: column; row-gap: 15px; list-style-type: none; align-items: flex-start; padding-left: 0px;";

                            {self.data}.forEach((el) => {{
                                const createListEl = document.createElement('li');

                                if ("{loadPageName}" === "None"){{
                                
                                    pageName_ = window.top.document.location.pathname.split("/");  
                                    pageName_ = pageName_[pageName_.length - 1]; 

                                    if (el.page_name === pageName_){{
                                        createListEl.id = "active";
                                        createListEl.style.backgroundColor = "green";
                                        createListEl.style.borderRadius = "0.2rem";    
                                        createListEl.style.display= "flex";
                                        createListEl.style.alignItems = "center";
                                        createListEl.style.columnGap = "8px";
                                        createListEl.style.color = "#0000005e";
                                        createListEl.style.cursor= "pointer";                              
                                        //createListEl.style.borderRadius = "2.5px";
                                    }} 
                                }}  else {{
                                            
                                    if (el.page_name === "{loadPageName}"){{
                                        createListEl.id = "active";
                                        createListEl.style.backgroundColor = "green";
                                        createListEl.style.borderRadius = "0.2rem";    
                                        createListEl.style.display= "flex";
                                        createListEl.style.alignItems = "center";
                                        createListEl.style.columnGap = "8px";
                                        createListEl.style.color = "#0000005e";
                                        createListEl.style.cursor= "pointer";                        
                                        //createListEl.style.borderRadius = "2.5px";
                                    }} 

                                }}

                                if (el.icon && el.iconLib !== "Google"){{
                                    const iconEl = document.createElement('i');
                                    iconEl.className = el.icon;
                                    iconEl.style.fontSize = "14px";
                                    iconEl.style.color = "black";
                                    createListEl.append(iconEl);
                                    //createListEl.appendChild(iconEl);
                                }} else if (el.icon && el.iconLib === "Google"){{
                                    const iconEl = document.createElement('i');
                                    iconEl.className = 'material-symbols-outlined';
                                    iconEl.innerText = el.icon;
                                    iconEl.style.fontSize = "14px";
                                    iconEl.style.color = "black";
                                    createListEl.append(iconEl);
                                }}

                                    const labelEl = document.createElement('div');
                                    labelEl.className = "navigation-label";
                                    labelEl.dataset.testid = el.page_name;
                                    labelEl.innerHTML = el.label;
                                    labelEl.style = "white-space:nowrap; display:table-cell;";
                                    labelEl.style.fontSize = "14px";
                                    labelEl.style.color = "black";

                                    createListEl.appendChild(labelEl);
                                    
                                    createListEl.className = "label-icon-container"; 
                                    navigationSelections.appendChild(createListEl);
                                    

                            }})

                            navigationSelectionsContainer.appendChild(navigationSelections);
                            newSidebar[0].appendChild(navigationSelectionsContainer);

                            const spaceDiv = document.createElement('div');
                            spaceDiv.style = "height: calc(41% - 1px); display: flex; align-items: flex-end; margin-bottom: 30px;";
                            newSidebar[0].appendChild(spaceDiv);
                            
                            const lineDivy = document.createElement('div');
                            const line = document.createElement('hr');
                            line.style = "borderTop: 0.2px solid #bbb;";
                            lineDivy.appendChild(line);
                            newSidebar[0].appendChild(lineDivy);

                            const profileDivContainer = document.createElement('div');
                            profileDivContainer.style = "display:flex; width:100%; justify-content:center; ";
                            const profileDiv = document.createElement('div');

                            const ImgSvg = document.createElementNS("http://www.w3.org/2000/svg", "svg"); //document.createElement('svg'); 
                            ImgSvg.setAttribute("width","70");
                            ImgSvg.setAttribute("height","70");                            

                            const ImgSvgCircle = document.createElementNS("http://www.w3.org/2000/svg", "circle"); //document.createElement('circle'); //createElementNS("http://www.w3.org/2000/svg", "circle");
                            ImgSvgCircle.setAttribute("fill","black");
                            ImgSvgCircle.setAttribute("cx","50%"); 
                            ImgSvgCircle.setAttribute("cy","50%");
                            ImgSvgCircle.setAttribute("r","30"); 

                            ImgSvg.appendChild(ImgSvgCircle);
                            profileDiv.appendChild(ImgSvg);
                            profileDivContainer.appendChild(profileDiv);

                            newSidebar[0].appendChild(profileDivContainer);

                            const userDetails = document.createElement("div");
                            userDetails.style = "width:100%; display: flex; flex-direction: column; align-items: flex-start;";
                            const userDetailsName = document.createElement("div");
                            userDetailsName.style = "width:100%; text-align:center;";
                            userDetailsName.innerText = "Daniel James";
                            const userDetailsEmail = document.createElement("div");
                            userDetailsEmail.style = "width:100%; text-align:center;";
                            userDetailsEmail.innerText = "daniel@gmail.com";

                            userDetails.appendChild(userDetailsName)
                            userDetails.appendChild(userDetailsEmail)
                            newSidebar[0].appendChild(userDetails);








                            

                            

                        }}
                    
                    </script> 

                '''
        st.components.v1.html(js_el, height=0, width=0)

        st.html(
            '''
                <style>
                    input[class='sidebar-search-bar']:focus{
                            outline:none;
                        }
                </style>
            '''
        )

    
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

        # //{self.storageChoice}.setItem("clickedPage", JSON.stringify({{"clickedPage":c.querySelectorAll('span')[0].getAttribute('data-testid')}})); //c.querySelectorAll('span')[0].innerHTML.toLowerCase()
        # //{self.storageChoice}.setItem("currentPage", JSON.stringify({{"currentPage":c.querySelectorAll('span')[0].getAttribute('data-testid')}}));

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
                 
    def loadCurrentPagePostClick(self):
        """
        Set current page after the page has been clicked.
        """
        if self.storageChoice == "localStorage":
            localS = LocalStorage()
            pageClicked = localS.getItem(itemKey="clickedPage")
            # if pageClicked != None:
            #     localS.setItem(itemKey="currentPage", itemValue=pageClicked)
        else:
            sessionS = SessionStorage(key="session_storage_init")
            pageClicked = sessionS.getItem(itemKey="clickedPage")
            # if pageClicked != None:
            #     sessionS.setItem(itemKey="currentPage", itemValue=pageClicked)
        
    def clicked_page(self, key="testing"):
        """
        Get the navigation user has just clicked
        """

        component_value = _component_func(initialPage=self.loadPageName, key=key, default=self.loadPageName)

        return component_value

    def change_page(self):

        """
        Changes page using streamlit's native `switch_page`. 
        """

        if "previousPage" not in st.session_state:
            st.session_state["previousPage"] = self.loadPageName
        else:
            st.session_state["previousPage"] = self.loadPageName

        if "currentPage" not in st.session_state:
            st.session_state["currentPage"] = self.clicked_page()
        else:
            st.session_state["currentPage"] = self.clicked_page()

        # clicked_page_ = self.clicked_page()
        # if st.session_state["currentPage"] != st.session_state["previousPage"]:
        #     print("DAAA", st.session_state["currentPage"], st.session_state["previousPage"]) 

        #     keyValList = [st.session_state["currentPage"]]
        #     expectedResult = [d for d in self.data if d['page_name'] in keyValList][0]
        #     st.switch_page(expectedResult["page_name_programmed"])

    # def change_page(self): 
    #     """
    #     Changes page using streamlit's native `switch_page`. Gets the value of the current page from local or session storage and then changes page accordingly.
    #     """

    #     # if "clickedPage" not in st.session_state:
    #     #     st.session_state["clickedPage"] = None 

    #     if self.storageChoice == "localStorage":
    #         localS = LocalStorage()
    #         pageSelect = localS.getItem(itemKey="currentPage")
    #         pageClicked = localS.getItem(itemKey="clickedPage")
    #     else:
    #         sessionS = SessionStorage(key="session_storage_init")
    #         pageSelect = sessionS.getItem(itemKey="currentPage")
    #         pageClicked = sessionS.getItem(itemKey="clickedPage")
        # print(pageClicked) 
        # print("storage", currentPage, "session_storage", st.session_state["currentPage"])
        # ["currentPage"]["page"]
        # if "storage" in st.session_state and st.session_state["storage"] != None and st.session_state["currentPage"]["page"] != currentPage["storage"]["currentPage"]:
            # st.write(currentPage["storage"])
        # if self.loadPageName != None:
        #     currentPage_ = self.loadPageName 
        # else:
        #     currentPage_ = pageSelect #["storage"]["currentPage"]

        # st.session_state["clickedPage"]
        
        # if pageClicked != None and pageClicked != st.session_state["clickedPage"]:
        #     print("previousPage", st.session_state["clickedPage"])
        #     st.session_state["clickedPage"] = pageClicked
        #     print( "clickedPage",pageClicked )

            # keyValList = [pageClicked]
            # expectedResult = [d for d in self.data if d['page_name'] in keyValList][0]
            # # print(expectedResult)
            # # print("currentPage_", currentPage_)
            # print(expectedResult["page_name_programmed"])
            # print("currentPage",pageSelect)
            # print("clickedPage", pageClicked)
            # st.switch_page(expectedResult["page_name_programmed"])

        #     print(pageClicked)
        
        #     keyValList = [pageClicked["clickedPage"]]
        #     expectedResult = [d for d in self.data if d['page_name'] in keyValList]
            
        #     print(expectedResult)

        
        # if pageSelect != None and currentPage_ != pageClicked["storage"]["currentPage"]:
        #     new_page = ""
        #     st.switch_page(pageSelect["storage"]["currentPage"])

        
    
    def load_custom_sidebar(self):
        """
        Salad of methods used to create final sidebar
        """
          
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
        self.clicked_page(key="change_page_test") 
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

        

