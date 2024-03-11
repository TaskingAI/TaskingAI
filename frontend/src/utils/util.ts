const findRouteByPath = (path:string, routes:any) => {
    let result = null;
  
    for (const route of routes) {
      if (path === route.path) {
        result = route;
        break;
      }
  
      if (path.startsWith(route.path)) {
        if (route.path === '/' && path.length === 1) {
          result = route;
          break;
        }
  
        if (route.children && route.children.length) {
          const remainingPath = path.slice(route.path.length);
          const foundChild:any = findRouteByPath(remainingPath, route.children);
          if (foundChild !== null) {
            result = foundChild;
            break;
          }
        } else {
          result = route;
          break;
        }
      }
    }
  
    return result;
  };
  const getFirstMethodAndEndpoint = (openapiJson:any) => {
    if (!openapiJson || !openapiJson.paths || !openapiJson.servers) {
      return null;
    }
    const baseUrl = openapiJson.servers[0].url; 
    const paths = Object.keys(openapiJson.paths);
  
    if (paths.length === 0) {
      return null;
    }
  
    const firstPath = paths[0]; 
    const methods = openapiJson.paths[firstPath]; 
    const firstMethod = Object.keys(methods)[0]; 
  
    return {
      method: firstMethod.toUpperCase(),
      endpoint: baseUrl + firstPath
    };
  }
  const formatTimestamp = (timestamp:number) => {
    const date = new Date(timestamp);
    const options: Intl.DateTimeFormatOptions  = { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false,month: 'short', day: 'numeric', year: 'numeric' };
    return new Intl.DateTimeFormat('en-US', options).format(date);
  }
  const formatTime = (timestamp: number) => {
    const date = new Date(timestamp);
  
    const options: any = { month: 'short', day: 'numeric', year: 'numeric' };
    return new Intl.DateTimeFormat('en-US', options).format(date);
  }
  const parseAndRenderText = (text:string) => {
    const linkRegex = /\[.*?\]\((.*?)\)/;
    const match = text.match(linkRegex);
    const apiDocumentationLink = match ? match[1] : null;
    if (apiDocumentationLink) {
      const renderedText = text.replace(linkRegex, (_match, linkText) => (
        `<a  className='href' href="${apiDocumentationLink}" target="_blank" rel="noopener noreferrer">${linkText}</a>`
      ));
      return renderedText;
    } else {
      return text;
    }
  };

  export { findRouteByPath, getFirstMethodAndEndpoint,formatTimestamp,parseAndRenderText,formatTime };
  