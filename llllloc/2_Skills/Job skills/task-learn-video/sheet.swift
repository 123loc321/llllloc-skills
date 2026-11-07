// sheet.swift - one contact sheet from up to 12 frames, with a text label on each tile. Apple's own drawing, no ffmpeg text filter needed
// (the Homebrew ffmpeg 9 on his Mac has no drawtext). Built once: swiftc -O sheet.swift -o sheet (study_video.py does this on first run).
// Run: ./sheet out.jpg cols rows tileW tileH image1 "label 1" image2 "label 2" ...
import AppKit
let a = CommandLine.arguments
guard a.count >= 8, let cols = Int(a[2]), let rows = Int(a[3]), let tw = Int(a[4]), let th = Int(a[5]) else {
    FileHandle.standardError.write("usage: sheet out.jpg cols rows tileW tileH image label [image label ...]\n".data(using: .utf8)!); exit(2)
}
let W = cols * tw, H = rows * th
guard let rep = NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: W, pixelsHigh: H, bitsPerSample: 8, samplesPerPixel: 4, hasAlpha: true,
                                 isPlanar: false, colorSpaceName: .deviceRGB, bytesPerRow: 0, bitsPerPixel: 0),
      let ctx = NSGraphicsContext(bitmapImageRep: rep) else { exit(3) }
NSGraphicsContext.saveGraphicsState(); NSGraphicsContext.current = ctx
NSColor(white: 0.25, alpha: 1).setFill(); NSRect(x: 0, y: 0, width: W, height: H).fill()
let font = NSFont.systemFont(ofSize: 16, weight: .medium)
let attrs: [NSAttributedString.Key: Any] = [.font: font, .foregroundColor: NSColor.white, .backgroundColor: NSColor(white: 0, alpha: 0.6)]
var i = 6, tile = 0
while i + 1 < a.count && tile < cols * rows {
    let col = tile % cols, row = tile / cols
    let x0 = CGFloat(col * tw), y0 = CGFloat(H - (row + 1) * th)   // AppKit counts from the bottom
    if let img = NSImage(contentsOfFile: a[i]), img.size.width > 0 {
        let s = min(CGFloat(tw) / img.size.width, CGFloat(th) / img.size.height)
        let w = img.size.width * s, h = img.size.height * s
        img.draw(in: NSRect(x: x0 + (CGFloat(tw) - w) / 2, y: y0 + (CGFloat(th) - h) / 2, width: w, height: h),
                 from: .zero, operation: .copy, fraction: 1)
    }
    NSAttributedString(string: " " + a[i + 1] + " ", attributes: attrs).draw(at: NSPoint(x: x0 + 6, y: y0 + CGFloat(th) - 24))
    i += 2; tile += 1
}
NSGraphicsContext.restoreGraphicsState()
guard let data = rep.representation(using: .jpeg, properties: [.compressionFactor: 0.85]) else { exit(4) }
do { try data.write(to: URL(fileURLWithPath: a[1])) } catch { FileHandle.standardError.write("cannot write \(a[1])\n".data(using: .utf8)!); exit(5) }
