# This code was written with support from Gemini on 2026-08-08

Jekyll::Hooks.register :site, :post_write do |site|
  data_dir = File.join(site.dest, '_data')
  FileUtils.mkdir_p(data_dir)
  FileUtils.cp_r(File.join(site.source, '_data/.'), data_dir)
end
