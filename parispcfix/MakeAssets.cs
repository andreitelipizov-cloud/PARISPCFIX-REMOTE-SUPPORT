using System;
using System.IO;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Drawing.Imaging;

class MakeAssets {
 static PointF[] Points(float[] values){PointF[] points=new PointF[values.Length/2];for(int i=0;i<points.Length;i++)points[i]=new PointF(8*values[i*2]+8,4*values[i*2+1]+12);return points;}
 static int Main(string[] args){try{string root=Path.GetFullPath(args[0]);using(Bitmap image=new Bitmap(256,256)){using(Graphics g=Graphics.FromImage(image)){g.Clear(Color.FromArgb(4,20,40));g.SmoothingMode=SmoothingMode.AntiAlias;using(Pen p=new Pen(Color.FromArgb(0,220,231),8)){p.LineJoin=LineJoin.Round;g.DrawLines(p,Points(new float[]{15,2,15,9,14,9,11,37,2,53,10,53,12,44,18,44,20,53,28,53,19,37,16,9,14,9}));p.Width=5;foreach(float[] line in new[]{new float[]{11,37,19,37},new float[]{12,28,18,28},new float[]{13,18,17,18},new float[]{10,41,20,31},new float[]{10,31,20,41}})g.DrawLines(p,Points(line));}}
 image.Save(Path.Combine(root,"flutter/assets/parispcfix-icon.png"),ImageFormat.Png);using(MemoryStream png=new MemoryStream()){image.Save(png,ImageFormat.Png);byte[] data=png.ToArray();using(BinaryWriter w=new BinaryWriter(File.Create(Path.Combine(root,"flutter/windows/runner/resources/parispcfix.ico")))){w.Write((ushort)0);w.Write((ushort)1);w.Write((ushort)1);w.Write((byte)0);w.Write((byte)0);w.Write((byte)0);w.Write((byte)0);w.Write((ushort)1);w.Write((ushort)32);w.Write(data.Length);w.Write(22);w.Write(data);}}}
 using(Image original=Image.FromFile(Path.Combine(root,"libs/portable/src/res/label.png")))using(Bitmap label=new Bitmap(original.Width,original.Height))using(Graphics g=Graphics.FromImage(label)){g.Clear(Color.Transparent);g.TextRenderingHint=System.Drawing.Text.TextRenderingHint.AntiAliasGridFit;float size=Math.Min(23,original.Height-4);Font font=new Font("Segoe UI",size,FontStyle.Bold,GraphicsUnit.Pixel);while(g.MeasureString("PARISPCFIX",font).Width>original.Width-4){font.Dispose();font=new Font("Segoe UI",--size,FontStyle.Bold,GraphicsUnit.Pixel);}using(font){SizeF measure=g.MeasureString("PARISPCFIX",font);using(Brush b=new SolidBrush(Color.FromArgb(0,220,231)))g.DrawString("PARISPCFIX",font,b,(original.Width-measure.Width)/2,(original.Height-measure.Height)/2);}label.Save(Path.Combine(root,"libs/portable/src/res/parispcfix-label.png"),ImageFormat.Png);}
 Console.WriteLine("Created PARISPCFIX icon and installer label.");return 0;}catch(Exception e){Console.Error.WriteLine(e);return 1;}}
}
