declare module '*.svg?react' {
    const content: React.FunctionComponent<React.SVGAttributes<SVGElement>>;
    export default content;
  }